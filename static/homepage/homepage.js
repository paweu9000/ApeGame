    function popitup(url) {
        newwindow=window.open(url,'monke','height=700,width=500');
        if (window.focus) {newwindow.focus()}
        return false;
    }
    

    function shoutbox(url) {
        shoutbox_window = window.open(url, 'shoutbox', 'height=720, width=1080');
        if (window.focus) {shoutbox_window.focus()}
        return false;
    }