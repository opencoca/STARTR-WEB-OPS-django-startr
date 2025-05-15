from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def smart_select_js():
    """
    Returns the JavaScript code for smart select functionality.
    """
    return mark_safe("""
    <script>
    // Cache for storing already processed options and elements
    const smartSelectCache = {
        convertedSelects: new WeakSet(),
        optionsCache: new Map()
    };

    function convertSelectToSmartSelect(originalSelect) {
        // Skip if already converted, hidden, or is a multiple select
        if (smartSelectCache.convertedSelects.has(originalSelect) || 
            originalSelect.classList.contains('smart-select-converted') || 
            originalSelect.style.display === 'none' ||
            originalSelect.offsetParent === null ||
            originalSelect.multiple) {
            return;
        }
        
        // Mark as converted both in class and cache
        originalSelect.classList.add('smart-select-converted');
        smartSelectCache.convertedSelects.add(originalSelect);

        const wrapper = document.createElement('div');
        wrapper.className = 'smart-select-wrapper';

        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = 'Type to filter...';
        input.setAttribute('autocomplete', 'off');
        input.className = 'smart-select-input';

        const list = document.createElement('ul');
        list.className = 'smart-options';
        list.style.display = 'none';  // Ensure hidden by default
        list.style.position = 'absolute';
        list.style.zIndex = '1001';
        list.style.width = '100%';
        list.style.maxHeight = '200px';
        list.style.overflowY = 'auto';
        list.style.backgroundColor = '#fff';
        list.style.border = '1px solid #ccc';
        list.style.padding = '0';

        // Get or create options from cache
        let options;
        const selectId = originalSelect.id || originalSelect.name || Math.random().toString(36).substring(2);
        
        if (smartSelectCache.optionsCache.has(selectId)) {
            // Use cached options
            const cachedData = smartSelectCache.optionsCache.get(selectId);
            options = cachedData.options;
            
            // Append cached list items
            cachedData.items.forEach(li => {
                list.appendChild(li.cloneNode(true));
            });
        } else {
            // Create options from the original select, filtering out empty choices
            const cachedItems = [];
            options = Array.from(originalSelect.options)
                .filter(option => option.textContent.trim() !== '---------')
                .map(option => {
                    const li = document.createElement('li');
                    li.textContent = option.textContent;
                    li.dataset.value = option.value;
                    
                    li.addEventListener('click', () => {
                        input.value = option.textContent;
                        originalSelect.value = option.value;
                        list.style.display = 'none';
                        
                        // Trigger change event on original select
                        const event = new Event('change', { bubbles: true });
                        originalSelect.dispatchEvent(event);
                    });
                    
                    list.appendChild(li);
                    cachedItems.push(li.cloneNode(true));
                    return li;
                });
                
            // Store in cache for future use
            smartSelectCache.optionsCache.set(selectId, {
                options: options,
                items: cachedItems
            });
        }

        // Set initial value only if an option is selected
        const selectedOption = originalSelect.options[originalSelect.selectedIndex];
        if (selectedOption && selectedOption.textContent.trim() !== '---------') {
            input.value = selectedOption.textContent;
        }

        // Using debounce for input filtering to avoid excessive processing
        let debounceTimeout;
        input.addEventListener('input', () => {
            clearTimeout(debounceTimeout);
            debounceTimeout = setTimeout(() => {
                const query = input.value.toLowerCase();
                let visible = 0;
                
                options.forEach((li, index) => {
                    const liElement = list.children[index];
                    if (liElement.textContent.toLowerCase().includes(query)) {
                        liElement.style.display = 'block';
                        visible++;
                    } else {
                        liElement.style.display = 'none';
                    }
                });
                
                // Only show list if there are visible options and input is focused
                list.style.display = (visible && document.activeElement === input) ? 'block' : 'none';
            }, 100); // 100ms debounce
        });

        // Show options on focus
        input.addEventListener('focus', () => {
            // Show all options when focused
            Array.from(list.children).forEach(li => li.style.display = 'block');
            list.style.display = 'block';
        });

        // Hide options on blur
        input.addEventListener('blur', () => {
            setTimeout(() => {
                list.style.display = 'none';
            }, 200);
        });

        // Handle keyboard navigation
        input.addEventListener('keydown', (e) => {
            const visibleOptions = Array.from(list.children).filter(li => li.style.display !== 'none');
            const currentIndex = visibleOptions.findIndex(li => li.classList.contains('highlighted'));
            
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                const nextIndex = (currentIndex + 1) % visibleOptions.length;
                visibleOptions.forEach(li => li.classList.remove('highlighted'));
                visibleOptions[nextIndex].classList.add('highlighted');
                visibleOptions[nextIndex].scrollIntoView({ block: 'nearest' });
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                const prevIndex = (currentIndex - 1 + visibleOptions.length) % visibleOptions.length;
                visibleOptions.forEach(li => li.classList.remove('highlighted'));
                visibleOptions[prevIndex].classList.add('highlighted');
                visibleOptions[prevIndex].scrollIntoView({ block: 'nearest' });
            } else if (e.key === 'Enter' && currentIndex >= 0) {
                e.preventDefault();
                visibleOptions[currentIndex].click();
            }
        });

        // Insert the new elements
        originalSelect.style.display = 'none';
        originalSelect.parentNode.insertBefore(wrapper, originalSelect);
        wrapper.appendChild(input);
        wrapper.appendChild(list);
        wrapper.appendChild(originalSelect);
    }

    function initSmartSelects() {
        // Use requestIdleCallback if available, otherwise use setTimeout
        // This helps prioritize critical rendering tasks
        const scheduleTask = window.requestIdleCallback || 
            (callback => setTimeout(callback, 1));
            
        scheduleTask(() => {
            // Process selects in batches to avoid blocking the main thread
            const processSelectBatch = (selects, startIndex, batchSize) => {
                const endIndex = Math.min(startIndex + batchSize, selects.length);
                
                for (let i = startIndex; i < endIndex; i++) {
                    convertSelectToSmartSelect(selects[i]);
                }
                
                if (endIndex < selects.length) {
                    scheduleTask(() => processSelectBatch(selects, endIndex, batchSize));
                }
            };
            
            const selects = Array.from(document.querySelectorAll(
                'select:not(.smart-select-converted):not([multiple])'
            ));
            
            processSelectBatch(selects, 0, 10); // Process 10 selects at a time
        });
    }

    // Initialize once the DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSmartSelects);
    } else {
        initSmartSelects();
    }

    // Set up a more efficient MutationObserver with throttling
    let pendingMutations = false;
    const observer = new MutationObserver((mutations) => {
        if (!pendingMutations) {
            pendingMutations = true;
            
            // Process mutations in the next animation frame to batch changes
            requestAnimationFrame(() => {
                let hasNewSelects = false;
                
                // Check if any new selects were added
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1) { // Element node
                            if (node.nodeName === 'SELECT') {
                                hasNewSelects = true;
                            } else if (node.querySelectorAll) {
                                hasNewSelects = hasNewSelects || 
                                    node.querySelectorAll('select:not(.smart-select-converted):not([multiple])').length > 0;
                            }
                        }
                    });
                });
                
                // Only initialize if new selects were found
                if (hasNewSelects) {
                    initSmartSelects();
                }
                
                pendingMutations = false;
            });
        }
    });

    // Start observing with more specific options to reduce overhead
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: false,
        characterData: false
    });
    </script>
    """)