<html>
    <head>
        <title>SCHOOL Game Design</title>
    </head>
    <body>
        <h1>SCHOOL Game Design</title>
        <?php
        
        $dirs = array_filter(glob("*"), "is_dir");
        print_r($dirs);
        
        ?>
    </body>
</html>
