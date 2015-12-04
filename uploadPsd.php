<?php

$filename = $_FILES ["files"] ["name"][0];
$filetype = $_FILES ["files"] ["type"][0];
$fileerror = $_FILES ["files"] ["error"][0];
$filetmpname = $_FILES ["files"] ["tmp_name"][0];

$allowedExts = array("psd");

$temp = explode(".", $filename);
$extension = strtolower(end($temp));
$name = preg_replace("/[^a-zA-Z0-9 ]+/", "", $temp [0]);

$result = 'failure';
$psd = null;

// File extension validation
if (in_array($extension, $allowedExts)) {
    $time = explode(".", microtime(true));
    $curTimeStamp = $time [0] . $time [1];
    $psdFileName = $filename . '_' . $curTimeStamp . '.psd';

    // if ($fileerror > 0) {
    // echo json_encode(array('result' => "fail"));
    // } else {
    if (file_exists('../specsFiles/' . $psdFileName)) {
        echo json_encode(array(
            'result' => "failure"
        ));
    } else {
        $moved = move_uploaded_file($filetmpname, '../specsFiles/' . $psdFileName);

        // call python
        $psd = exec("python read_psd_module.py " . $psdFileName);
        /*if ($psd != null) {
            $psd = json_decode($psd, true);
            for ($i = 0; $i < sizeof($psd["layers"]); $i++) {
                $f = exec("python read_psd_image_module.py " . $psd["layers"][$i]["image"]);
                $psd["layers"][$i]["image_base"] = $f;
            }
        }*/
        $result = 'success';
    }
} else {
    echo json_encode(array(
        'result' => "fail"
    ));
}

header('Content-type: application/json');
echo json_encode(array(
    'result' => $result,
    'data' => json_decode($psd, true)
));
