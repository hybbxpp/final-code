/**
 * Created by Jill on 16/11/19.
 * @author :  jill
 * @jill's blog : http://blog.csdn.net/jill6693484
 */

function chat(element, imgSrc, doctextContent, userid) {
    //判断传入的值，是医生还是患者
    var $user = element;
    //var $doctorHead = imgSrc;
    //获取输入的值
    var $textContent = $('.chat-info').html();
    //获取传入的医生输入的内容
    var $doctextContent = doctextContent;
    //获取容器
    var $box = $('.bubbleDiv');
    //var $boxHeght = $box.height();
    //var $sectionHeght = $(".chat-box").height();
    //var $elvHeght = Math.abs($boxHeght - $sectionHeght);
    //医生
    if ($user === "leftBubble") {
        var $block = createdoct(imgSrc, $doctextContent);
        if ($block) {
            $box.append($block).animate({scrollTop: 1000000000}, 300);
        }
    }
    //患者
    else if ($user === "rightBubble") {
        var $block = createuser($textContent);
        if ($block) {
            $box.append($block).animate({scrollTop: 1000000000}, 300);
        }
    } else {
        console.log("请传入必须的参数");
    }
}

function createdoct(imgSrc, $doctextContent) {
    var $textContent = $doctextContent;
    var block;
    if ($textContent === '' || $textContent === 'null') {
        // alert('亲！别太着急，先说点什么～');
        return null;
    }

    //这里通过聊天中的数据获得需要显示的文件名
    // block = '<div class="bubbleItem">' +
    //     '<div class="doctor-head">' +
    //     '<img src="' + imgSrc + '" alt="doctor"/>' +
    //     '</div>' +
    //     '<span class="bubble leftBubble">' + $textContent + '<span class="topLevel"></span></span>';

    // block += '</div>';

    $textContent = $textContent.replace(/\n+/g, '<br/>');
    var reg = /(\w+\.(?:jpeg|png))/g;
    if(reg.test($textContent))
    {
        $textContent = $textContent.replace(reg, '<br/><p>&nbsp;&nbsp;&nbsp;&nbsp;</p><img src="/static/images/illustration/$1"/>');
    }
    block = '<div class="bubbleItem">' +
        '<div class="doctor-head">' +
        '<img src="' + imgSrc + '" alt="doctor"/>' +
        '</div>' +
        '<span class="bubble leftBubble">' + $textContent + '<span class="topLevel"></span></span>' + 
        '</div>';
    return block;
};

function createuser($text) {
    var $textContent = $text;
    var block;
    if ($textContent === '' || $textContent === 'null') {
        // alert('亲！别太着急，先说点什么～');
        return null;
    }
    block = '<div class="bubbleItem clearfix">' +
        '<span class="bubble rightBubble">' + $textContent + '<span class="topLevel"></span></span>' +
        '</div>';

    return block;
};
