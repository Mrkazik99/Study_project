<!DOCTYPE html>
<html>
    <head>
        <title>Test</title>
    </head>
    <body>
        <?php
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $this->'python_api/service/api/test');
            $result = curl_exec($ch);
            $result = @json_decode($result);
            print($result);
        ?>
    </body>
</html>