// Lazy loading functionality for Django Admin inlines
document.addEventListener('DOMContentLoaded', function() {
    // Cache DOM lookups and reused elements
    const csrf_token = document.querySelector('[name="csrfmiddlewaretoken"]')?.value;
    const admin_form = document.querySelector('#content-main form');
    
    // Extract the object_id from the URL path
    // Expected URL format: /admin/app_label/model_name/object_id/change/
    const urlParts = window.location.pathname.split('/').filter(Boolean);
    const objectIdPosition = urlParts.length - 2; // Second to last part, before 'change'
    const object_id = urlParts[objectIdPosition];
    
    console.log('URL parts:', urlParts);
    console.log('Using object ID:', object_id);
    
    // Special handling for groups which might have many participants
    const isGroupAdmin = window.location.pathname.includes('/admin/experiences/group/');
    
    // Find all lazy-loading inline groups (marked by the backend)
    const inlineGroups = document.querySelectorAll('.inline-group[data-lazy-load="true"]');
    
    // Keep track of loaded inlines to prevent duplicate AJAX requests
    const loadedInlines = new Set();
    
    // Detect if we're on a Group change page and add special optimizations
    if (isGroupAdmin) {
        console.log('Optimizing admin for Group with lazy-loaded participants');
    }
    
    // Process each inline group
    inlineGroups.forEach(function(group) {
        const inlineType = group.dataset.inlineType;
        const modelName = group.dataset.model;
        const inlineName = group.dataset.name;
        const relatedField = group.dataset.rel || 'id';
        const recordCount = parseInt(group.dataset.count || '0', 10);
        
        // Mark the group as pending lazy load
        group.classList.add('lazy-loading-pending');
        
        // Create a placeholder to show instead
        const placeholder = document.createElement('div');
        placeholder.className = 'lazy-inline-placeholder';
        placeholder.id = `placeholder-${group.id}`;
        
        // Use a more informative message for groups with many participants
        let message = 'This section is lazy-loaded to improve page performance.';
        if (isGroupAdmin && modelName === 'participation' && recordCount > 20) {
            message = `This group has ${recordCount} participants. Loading them all at once can slow down the page.`;
        }
        
        // Show count if available
        let countHtml = '';
        if (recordCount > 0) {
            countHtml = `<span class="lazy-inline-counter">${recordCount} item${recordCount !== 1 ? 's' : ''}</span>`;
        }
        
        placeholder.innerHTML = `
            <h3>${inlineName} ${countHtml}</h3>
            <p>${message}</p>
            <button type="button" class="lazy-inline-button" data-target="${group.id}">
                Load ${inlineName} data
            </button>
        `;
        
        // Insert placeholder before the group
        group.parentNode.insertBefore(placeholder, group);
        
        // Add click handler for the load button
        const loadButton = placeholder.querySelector('.lazy-inline-button');
        loadButton.addEventListener('click', function() {
            const targetId = this.dataset.target;
            
            // If already loaded, just show it
            if (loadedInlines.has(targetId)) {
                showInlineGroup(targetId, placeholder);
                return;
            }
            
            // Update placeholder to show loading state
            placeholder.innerHTML = `
                <div class="lazy-inline-loading">
                    <div class="lazy-inline-spinner"></div>
                    <span>Loading ${inlineName} data...</span>
                </div>
            `;
            
            // Fetch the inline content via AJAX
            fetchInlineContent(group, placeholder);
        });
    });
    
    /**
     * Fetches the inline content from the server
     */
    function fetchInlineContent(group, placeholder) {
        const inlineType = group.dataset.inlineType;
        const modelName = group.dataset.model;
        const app = group.dataset.app;
        
        // Create a URL that will fetch just this inline
        const url = `/admin/lazy-inline/${app}/${modelName}/${object_id}/`;
        
        console.log('Fetching lazy inline content from URL:', url);
        console.log('Data:', {
            inlineType: inlineType,
            modelName: modelName,
            app: app,
            objectId: object_id
        });
        
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrf_token,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `inline_type=${inlineType}&parent_id=${object_id}`
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(html => {
            // Replace the inline group's content with the fetched HTML
            group.innerHTML = html;
            
            // Run any initialization scripts that might be in the response
            const scripts = Array.from(group.querySelectorAll('script'));
            scripts.forEach(oldScript => {
                const newScript = document.createElement('script');
                Array.from(oldScript.attributes).forEach(attr => {
                    newScript.setAttribute(attr.name, attr.value);
                });
                newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                oldScript.parentNode.replaceChild(newScript, oldScript);
            });
            
            // Mark as loaded and show the group
            loadedInlines.add(group.id);
            showInlineGroup(group.id, placeholder);
            
            // Initialize any Django admin widgets
            if (window.django && window.django.jQuery) {
                window.django.jQuery(document).trigger('formset:added');
            }
        })
        .catch(error => {
            console.error('Error loading inline content:', error);
            placeholder.innerHTML = `
                <div class="lazy-inline-placeholder">
                    <p>Error loading ${group.dataset.name}. Please try again.</p>
                    <button type="button" class="lazy-inline-button" data-target="${group.id}">
                        Retry
                    </button>
                </div>
            `;
            
            // Re-attach click handler
            placeholder.querySelector('.lazy-inline-button').addEventListener('click', function() {
                fetchInlineContent(group, placeholder);
            });
        });
    }
    
    /**
     * Shows an inline group and removes its placeholder
     */
    function showInlineGroup(groupId, placeholder) {
        const group = document.getElementById(groupId);
        group.classList.remove('lazy-loading-pending');
        placeholder.remove();
    }
    
    /**
     * Lazy loads inlines when the tab is clicked (for tabbed admin interfaces)
     */
    if (document.querySelector('.admin-tabs')) {
        const tabs = document.querySelectorAll('.admin-tabs a');
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                const tabId = this.getAttribute('href');
                const tabPanel = document.querySelector(tabId);
                
                if (tabPanel) {
                    const pendingInlines = tabPanel.querySelectorAll('.lazy-inline-button');
                    // Auto-load any inlines in this tab
                    pendingInlines.forEach(button => {
                        setTimeout(() => button.click(), 100);
                    });
                }
            });
        });
    }
});
