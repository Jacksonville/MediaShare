<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Image Sharer</title>
    <link rel="stylesheet" href="/static/css/bootstrap.css" />
    <link rel="stylesheet" href="/static/css/jquery.fancybox.css" />
    <style type="text/css">
        .column {
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
          <div class="col-md-12 col-lg-12">
            <h1>Image Sharer</h1>
          </div>
        </div>
        <div class="row">
            <div class="col-md-12 col-lg-12">
                <a href="/?dir={{curr_dir[:-1].replace(curr_dir[:-1].split('/')[-1],'')[:-1].replace('///','/').replace('//','/')}}">Up</a>
            </div>
        </div>
        %for dir in dirlist:
        <div class="row">
            <div class="col-md-12 col-lg-12">
                <a href="/?dir={{curr_dir.replace('///','/').replace('//','/')}}{{dir.replace('///','/').replace('//','/')}}">{{dir}}</a>
            </div>
        </div>
        %end
        %import os
        %for file in sorted(set(filelist)):
            %if os.path.splitext(file)[1][1:].lower() in ['jpg', 'jpeg', 'bmp', 'png']:
                <div class="column thumbnail" style="white-space: normal;">
                    <a class="fancybox" rel="ligthbox" href="/static/images/temp/{{curr_dir[1:].replace('/','_')}}{{file}}">
                        <img data-original="/static/images/temp/thumb_{{curr_dir[1:].replace('/','_')}}{{file}}" class="lazy" width="320" height="320">
                        <div class="caption">
                            <p>{{file}}</p>
                        </div>
                    </a>
                </div>
            %end
        %end
    </div>
    <script src="/static/js/jquery-2.1.3.js"></script>
    <script src="/static/js/bootstrap.js"></script>
    <script src="/static/js/jquery.lazyload.min.js"></script>
    <script src="/static/js/jquery.fancybox.js"></script>
    <script>
      $(function(){
          $("img.lazy").lazyload({threshold : 200});
          $(".fancybox").fancybox({
            openEffect: "none",
            closeEffect: "none"
          });
      });
    </script>
</body>
</html>
