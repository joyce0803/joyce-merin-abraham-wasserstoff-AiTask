<?php
/*
Plugin Name: AI Chatbot
Plugin URI: http://yourwebsite.com/ai-chatbot
Description: A simple AI chatbot that appears when a button is clicked.
Version: 1.0
Author: Your Name
Author URI: http://yourwebsite.com
*/

// Hook for adding admin menus
add_action('wp_enqueue_scripts', 'ai_chatbot_enqueue_scripts');
add_action( 'wp_footer', 'ai_chatbot_shortcode');

// Load JavaScript and CSS for Chatbot
function ai_chatbot_enqueue_scripts() {
    wp_enqueue_style('ai-chatbot-css', plugins_url('ai-chatbot.css', __FILE__));
    wp_enqueue_script('ai-chatbot-js', plugins_url('ai-chatbot.js', __FILE__), array('jquery'), null, true);
    wp_localize_script('ai-chatbot-js', 'aiChatbot', array(
        'loadDataUrl' => 'https://joyce-merin-abraham-wasserstoff-aitask.onrender.com/load_data'
    ));
}


// Shortcode to display chatbot button and container
function ai_chatbot_shortcode() {
    $content = '<button id="chatbot-toggle-button" class="sticky-slider" onclick="aiChatbotToggle()"><img src="https://cdn-icons-png.flaticon.com/512/5356/5356190.png" style="height:40px; width:40px;"></img></button>';
    $content .= '<div id="ai-chatbot-container" style="display:none;">';
    $content .= '<div id="ai-chatbot-close" onclick="aiChatbotToggle()">x</div>';
    $content .= '<iframe src="https://joyce-merin-abraham-wasserstoff-aitask.onrender.com/" frameborder="0" width="420" height="650"></iframe>';
    $content .= '</div>';
    return $content;
}
add_shortcode('ai_chatbot', 'ai_chatbot_shortcode');
