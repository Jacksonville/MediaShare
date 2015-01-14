<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Media Share</title>
    <link rel="stylesheet" href="/static/css/foundation.css" />
    <script src="/static/js/vendor/modernizr.js"></script>
    <script src="/static/js/vendor/jquery.js"></script>
    <script src="/static/js/jquery.multiDownload.js"></script>
</head>
<body>
    <div class="row">
      <div class="large-12 columns">
        <h1>Media Share</h1>
      </div>
    </div>
    <div class="row">
        <a href="/?dir={{curr_dir[:-1].replace(curr_dir[:-1].split('/')[-1],'')[:-1].replace('///','/').replace('//','/')}}">Up</a>
    </div>
    %for dir in dirlist:
    <div class="row">
        <a href="/?dir={{curr_dir.replace('///','/').replace('//','/')}}{{dir.replace('///','/').replace('//','/')}}">{{dir}}</a>
    </div>
    %end
    <ul id="thumbs" class="clearing-thumbs" data-clearing>
    %import os
    %for file in sorted(set(filelist)):
        %if os.path.splitext(file)[1][1:].lower() in ['jpg', 'jpeg', 'bmp', 'png']:
            <li><a class="th" href="/static/images/temp/{{curr_dir[1:].replace('/','_')}}{{file}}"> <img data-original="/static/images/temp/thumb_{{curr_dir[1:].replace('/','_')}}{{file}}" class="lazy" width="320" height="320"> </a></li>
        %end
    %end
    </ul>
    <script src="/static/js/vendor/jquery.js"></script>
    <script src="/static/js/foundation.min.js"></script>
    <script src="/static/js/jquery.lazyload.js"></script>
    <script>
      $(function(){
          $(document).foundation();
          $("img.lazy").lazyload({threshold : 200});
      });
      
    </script>
</body>
</html>
