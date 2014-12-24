$(function() {
    // read the url query string
    var qs = readQS();
    var data = parseQS(qs);
    // fill in title
    $("#title").text(data.title);
    // fill in content (from url)

    // edit/done buttons
    $('#edit-btn').click(function() {
        $(this).hide();
        $('#done-btn').show();
        $('.bubble').prop('readonly', false);
        $('#edit-td').show();
        $("#content-pane").sortable("enable");
        $('.delete-btn').show();
        $('.bubble-text, #title').prop('readonly', false);
        $('#share').attr('href', '').text('');
    });
    $('#done-btn').click(function() {
        $(this).hide();
        $('#edit-btn').show();
        $('.bubble').prop('readonly', true);
        $('#edit-td').hide();
        $("#content-pane").sortable("disable");
        $('.delete-btn').hide();
        $('.bubble-text, #title').prop('readonly', true);
        showUrl();
    });
    $('#clear-btn').click(function() {
        $('#content-pane').children('li').remove();
    });
    initedit();

    updateContent(data, '#content-pane');
    $('.bubble-text').autosize();
});

function showUrl() {
    var result = [];
    $('#content-pane li').each( function(i) {
        var child = $(this).children().first();
        if(child.is('img')) {
            //trim 'images/' and '.jpg'
            var src = child.attr('src')
                .replace(/\.[^/.]+$/, "")
                .replace(/.*images[/]/, "");
            result.push('i' + i + '=' + src);
        } else if (child.is('.bubble')) {
            child = child.children('.bubble-text').first();
            result.push('t' + i + '=' + encodeURIComponent(child.val()));
        }
    });
    var title = $('#title').val();
    if (title)
        result.push('title=' + encodeURIComponent(title));

    var s = location.protocol + '//' + location.host
            + location.pathname;
    if (result.length) {
        s += '?' + result.join('&');
    }
    $('#share').attr('href', s).text('link');
}

function initedit() {
    $("#content-pane").sortable({
        disabled:true,
        update: function(event, ui) {
            // hack : reset of the width and height
            ui.item.width('');
            ui.item.height('');

            // if img
            var el = ui.item.children().first();
            if(el.is('img')) {
                var path = el.attr('src');
                // if thumbnail change to non-thumbnail
                if (path.endsWith('_t.jpg')) {
                    var sp = path.split('_t.jpg');
                    el.attr('src', sp[0] + '.jpg');
                }
            }
            // add the delete button if necessary
            if (!ui.item.children('.delete-btn').length) {
                ui.item.append(deleteButton);
            }
            if (el.hasClass('bubble')) {
                if(!el.children('.bubble-text').length) {
                    el.append('<textarea class="bubble-text"></textarea>');
                    el.children('.bubble-text').autosize();
                }
                setClickDraggable(el);
            }
            ui.item.children('.delete-btn').show();
            ui.item.removeClass('edit-item');
        }
    });

    // add generic bubble in edit-pane
    $("#edit-pane").append(
        '<li class="edit-item"><div class="bubble"></div></li>');

    // fill the edit pane with images
    getImages(location.pathname + "images/", "_t.jpg", '#edit-pane', function(){
        // make the edit pane images draggable
        $('#edit-pane').children().draggable({
            helper: 'clone',
            // opacity: .5,
            connectToSortable: '#content-pane'

        });

        // add delete buttons
        $('.content-item').append(deleteButton);
        // $('.content-item').has('.bubble').append(editButton);
        // $('.content-item').has('.bubble').append(editDoneButton);
        setClickDraggable($('.bubble'));
    });
}


function setClickDraggable(bubbleEl) {
    bubbleEl.on('mousedown', function(e) {
        // http://stackoverflow.com/a/22838495
        var mdown = document.createEvent('MouseEvents');
        mdown.initMouseEvent('mousedown', true, true, window, 0, e.screenX,
                e.screenY, e.clientX, e.clientY, true, false, false, true, 0,
                null);
        $(this).closest('li')[0].dispatchEvent(mdown);
    });
}

function deleteClick(btn) {
    $(btn).parent().remove();
}


function updateContent(data, where) {
    $(where).html('');
    for(i=0; i < data.content.length; ++i) {
        $(where).append('<li class="content-item">' + contentToHtml(data.content[i])
        + "</li>");
    }
}

// http://stackoverflow.com/a/3855394
function readQS() {
    a = window.location.search.substr(1).split('&');
    if (a == "") return {};
    var b = {};
    for (var i = 0; i < a.length; ++i)
    {
        var p=a[i].split('=', 2);
        if (p.length == 1)
            b[p[0]] = "";
        else
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
    }
    return b;
}

function parseQS(qs) {
    var result = {};
    result.title = qs.title;
    result.content = [];
    var i=0;
    while(true) {
        if ("i"+i in qs)
            result.content.push({
                type: "image",
                url: "images/" + qs["i"+i] + ".jpg"});
        else if("t"+i in qs)
            result.content.push({
                type: "text",
                text: qs["t"+i]});
        else
            break;
        ++i;
    }
    return result;
}

function contentToHtml(el) {
    if (el.type == "image") {
        return '<img src="' + el.url + '">';
    } else if (el.type == "text") {
        var text = el.text;
        return '<div class="bubble"><textarea class="bubble-text" readonly>' + text + "</textarea></div>";
    } else {
        console.log("wrong element type (image and text supported)");
    }
}

var deleteButton =
    '<input class="delete-btn" value="x" type="button" style="display:none" onclick="deleteClick(this)">';

function getImages(dir, ext, appendTo, cb) {
    $.ajax({
    //This will retrieve the contents of the folder if the folder is
    // configured as 'browsable'
    url: dir,
    success: function (data) {
        //List all file names in the page
        $(data).find("a:contains(" + ext + ")").each(function () {
            var filename = $(this).attr('href');
            $(appendTo).append(
                '<li class="edit-item"><img src="' + dir + filename + '"></li>');
        });
        cb();
    }
    });
}

String.prototype.endsWith = function(suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};
