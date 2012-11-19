//-------------------------------------------------
//      youtube playlist jquery plugin
//      Created by dan@geckonm.com
//      www.geckonewmedia.com
//
//      v1.1 - updated to allow fullscreen
//           - thanks Ashraf for the request
//-------------------------------------------------

(function ($) {
jQuery.fn.ytplaylist = function(options) {

  // default settings
  var options = jQuery.extend( {
    holderId: 'ytvideo',
    playerHeight: '300',
    playerWidth: '450',
    addThumbs: false,
    thumbSize: 'small',
    showInline: false,
    autoPlay: true,
    showRelated: true,
    allowFullScreen: false,
    showPlayer: true,
  videolinkattribute: 'href'
  },options);

  return this.each(function() {

    var selector = $(this);

    var autoPlay = "";
        var showRelated = "&rel=0";
        var fullScreen = "";
        if(options.autoPlay) autoPlay = "&autoplay=1";
        if(options.showRelated) showRelated = "&rel=1";
        if(options.allowFullScreen) fullScreen = "&fs=1";

    //grab a youtube id from a (clean, no querystring) url (thanks to http://jquery-howto.blogspot.com/2009/05/jyoutube-jquery-youtube-thumbnail.html)
    function youtubeid(url) {
      var myregexp = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/ ]{11})/i;
      var videoID = url.match(myregexp);
      // var ytid = url.match("[\\?&]v=([^&#]*)");
      videoID = videoID[1];
      return videoID;
    };

        if (options.showPlayer){
            //throw a youtube player in
            // function play(id, description)
            // {
            //    description = description ? description : 'No flash';
            //    var s1 = new SWFObject("http://www.youtube.com/v/"+id+autoPlay+showRelated+fullScreen,"prodotti",options.playerWidth,options.playerHeight,"7");
            //    s1.addVariable("width",options.playerWidth);
            //    s1.addVariable("height",options.playerHeight);
            //    if(options.allowFullScreen) {
            //         s1.addParam("wmode","transparent");
            //    }
            //    s1.addParam("wmode","transparent");
            //    s1.addVariable("transition","fade");
            //    $('#'+options.holderId).html(description);
            //    s1.write(options.holderId);

            // };
            function play(id, description)
            {
               description = description ? description : 'No flash';
               var iframe = $('<iframe src="http://www.youtube.com/embed/'+id+'" frameborder="0" allowfullscreen></iframe>');
               $('#'+options.holderId).html(iframe);
            };


            //load inital video
            var firstVid = selector.children("li:first-child").addClass("currentvideo").children("a").attr(options.videolinkattribute);
            var description = selector.children("li:first-child").addClass("currentvideo").children("a").attr("title");
            play(youtubeid(firstVid), description);


        //load video on request
        selector.children("li").children("a").click(function() {

            if(options.showInline) {
                $("li.currentvideo").removeClass("currentvideo");
                $(this).parent("li").addClass("currentvideo")
                play(youtubeid($(this).attr(options.videolinkattribute)), $(this).attr("title"));
            }
            else {
                play(youtubeid($(this).attr(options.videolinkattribute)), $(this).attr("title"));
                $(this).parent().parent("ul").find("li.currentvideo").removeClass("currentvideo");
                $(this).parent("li").addClass("currentvideo");
            }

            return false;
        });
    }

        //do we want thumns with that?
        if(options.addThumbs) {

            selector.children().each(function(i){
                console.log($(this).children("a").attr(options.videolinkattribute));
                var replacedText = $(this).children("a").text();
                var altText = $(this).children("a").attr('title');

                if(options.thumbSize == 'small') {
                    var thumbUrl = "http://img.youtube.com/vi/"+youtubeid($(this).children("a").attr(options.videolinkattribute))+"/2.jpg";
                }
                else {
                    var thumbUrl = "http://img.youtube.com/vi/"+youtubeid($(this).children("a").attr(options.videolinkattribute))+"/0.jpg";
                }


                $(this).children("a").empty().html("<img src='"+thumbUrl+"' alt='"+altText+"' />"+replacedText).attr("title", altText);

            });

        }



  });

};
}(jQuery));