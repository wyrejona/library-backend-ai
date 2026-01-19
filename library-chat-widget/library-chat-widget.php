<?php
/**
 * Plugin Name: Library AI Assistant
 * Description: A floating chat widget powered by your FastAPI backend.
 * Version: 1.0
 * Author: Library Team
 */

if (!defined('ABSPATH')) exit;

function lcw_enqueue_scripts() {
    wp_enqueue_style('lcw-style', plugin_dir_url(__FILE__) . 'style.css');
    wp_enqueue_script('lcw-script', plugin_dir_url(__FILE__) . 'script.js', array('jquery'), '1.0', true);

    wp_localize_script('lcw-script', 'lcwSettings', array(
        'apiUrl' => 'http://127.0.0.1:8000/ask',
        'nonce'  => wp_create_nonce('lcw_nonce')
    ));
}
add_action('wp_enqueue_scripts', 'lcw_enqueue_scripts');

function lcw_add_chat_html() {
    ?>
    <div id="lcw-container">
        <button id="lcw-toggle-btn">
            <span class="dashicons dashicons-format-chat"></span> Chat with Library AI
        </button>
        <div id="lcw-chat-window" style="display: none;">
            <div class="lcw-header">
                <h3>Library Assistant</h3>
                <button id="lcw-close-btn">&times;</button>
            </div>
            <div id="lcw-messages">
                <div class="lcw-message bot">
                    Hello! I can answer questions about library hours, policies, and referencing styles. How can I help?
                </div>
            </div>
            <div class="lcw-input-area">
                <input type="text" id="lcw-input" placeholder="Type a question..." />
                <button id="lcw-send-btn">Send</button>
            </div>
        </div>
    </div>
    <?php
}
add_action('wp_footer', 'lcw_add_chat_html');
