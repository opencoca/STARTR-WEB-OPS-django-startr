// Debug helper for lazy inlines
// Add this to your lazy_inlines.js or include as a separate file

console.log('Debug helper for lazy inlines loaded');

// Function to inspect the DOM structure for lazy loading
function debugLazyInlines() {
    console.log('Analyzing lazy inline setup...');
    
    // 1. Check if the template is loaded
    const templateLink = document.querySelector('link[href*="lazy_inlines.css"]');
    console.log('Template CSS loaded:', templateLink ? 'Yes' : 'No');
    
    const scriptTag = document.querySelector('script[src*="lazy_inlines.js"]');
    console.log('Template JS loaded:', scriptTag ? 'Yes' : 'No');
    
    // 2. Check for inline groups with lazy-load attribute
    const lazyGroups = document.querySelectorAll('[data-lazy-load="true"]');
    console.log('Found lazy-load groups:', lazyGroups.length);
    
    if (lazyGroups.length > 0) {
        lazyGroups.forEach((group, index) => {
            // Log each lazy group's data attributes
            console.log(`Group ${index + 1}:`, {
                id: group.id,
                inlineType: group.dataset.inlineType || 'MISSING',
                app: group.dataset.app || 'MISSING',
                model: group.dataset.model || 'MISSING',
                name: group.dataset.name || 'MISSING',
                count: group.dataset.count || 'MISSING'
            });
        });
    } else {
        // Check if there are any inline groups that should be lazy
        const allInlineGroups = document.querySelectorAll('.inline-group');
        console.log('Total inline groups found:', allInlineGroups.length);
        
        // Log details of all inline groups
        allInlineGroups.forEach((group, index) => {
            console.log(`Regular Inline ${index + 1}:`, {
                id: group.id,
                classList: Array.from(group.classList),
                hidden: group.style.display === 'none',
                attributes: Array.from(group.attributes).map(attr => `${attr.name}="${attr.value}"`)
            });
        });
    }
    
    // 3. Check for placeholders
    const placeholders = document.querySelectorAll('.lazy-inline-placeholder');
    console.log('Found placeholders:', placeholders.length);
    
    // 4. Check if any buttons have been created
    const buttons = document.querySelectorAll('.lazy-inline-button');
    console.log('Found lazy-load buttons:', buttons.length);
    
    return 'Debug complete - check the console for results';
}

// Run the debug helper after page load
document.addEventListener('DOMContentLoaded', function() {
    // Wait a second to ensure everything else has loaded
    setTimeout(debugLazyInlines, 1000);
    
    // Add a global function for manual debugging
    window.debugLazyInlines = debugLazyInlines;
    
    // Add console message to explain how to trigger manual debug
    console.log('Debug helper loaded. Run debugLazyInlines() in console to analyze lazy inline setup.');
});
