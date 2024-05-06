function aiChatbotToggle() {
    var chatContainer = document.getElementById('ai-chatbot-container');
    var toggleButton = document.getElementById('chatbot-toggle-button');
    if (chatContainer.style.display === 'none') {
        chatContainer.style.display = 'block';
        toggleButton.style.display = 'none';
    } else {
        chatContainer.style.display = 'none';
        toggleButton.style.display = 'block';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var chatButton = document.getElementById('.sticky-slider');
    if (chatButton) {
        chatButton.addEventListener('click', function() {
            aiChatbotToggle();
            loadChatbotData();
        });
    }
});


function loadChatbotData() {
    console.log("Loading chatbot data..."); 

    // Fetch posts
    jQuery.get("https://typical-hands.localsite.io/wp-json/wp/v2/posts", function(posts) {
        // Extract rendered content from each post
        const postsContent = posts.map(post => post.content.rendered);

        // Fetch pages
        jQuery.get("https://typical-hands.localsite.io/wp-json/wp/v2/pages", function(pages) {
            // Extract rendered content from each page
            const pagesContent = pages.map(page => page.content.rendered);

            // Prepare data with content only from posts and pages
            var data = {
                posts: postsContent,
                pages: pagesContent
            };

            // Send the content-only data to the Flask app
            jQuery.ajax({
                url: "https://joyce-merin-abraham-wasserstoff-aitask.onrender.com/load_data",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(data),
                success: function(response) {
                    console.log("Data loaded into chatbot", response);
                },
                error: function(xhr, status, error) {
                    console.error("Failed to load data into chatbot", xhr, status, error);
                }
            });
        });
    });
}

