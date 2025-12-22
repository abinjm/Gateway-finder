<?php

$botToken = "8354463122:AAF9nR5ePOHFdGYPUPglqypAraar-CqH6PY";
$checkerUrl = "https://test.infinitemsfeed.com/chk.php?lista=";

$update = json_decode(file_get_contents('php://input'), true);

if(isset($update['message'])){
    $chatId = $update['message']['chat']['id'];
    $message = $update['message']['message_id'];
    $text = $update['message']['text'];

    if(strpos($text, '/chk') === 0){
        $waitMsg  = sendMessage($chatId, "Checking... Card", $messageId);

        $cc = trim(str_replace('/chk ', '', $text));

        if(empty($cc)){
            editMessage($chatId, $waitMsg, "Please provide a valid card number");
            exit();
        }

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $checkerUrl . $cc);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

        $result = curl_exec($ch);
        curl_close($ch);

        $result = json_decode($result, true);

        $response = "Card: " . $cc . "\n\n";
if (isset($result['success'])) {

    if ($result['success'] === true) {

        $response .= "𝗦𝘁𝗮𝘁𝘂𝘀 - Approved ✅\n";
        $response .= "━━━━━━━━━━━━━\n";
        $response .= "[ϟ] 𝗜𝗡𝗣𝗨𝗧 ⌁ {$value}\n";
        $response .= "[ϟ] 𝗦𝘁𝗮𝘁𝘂𝘀 : " . ($result['message'] ?? "Approved") . " ✅\n";
        $response .= "[ϟ] 𝗚𝗮𝘁𝗲 - API Check\n";
        $response .= "━━━━━━━━━━━━━\n";
        $response .= "[ϟ] 𝗦𝗰𝗿𝗮𝗽𝗽𝗲𝗱 𝗕𝘆 : @abinjmoffical\n";

    } else {

        $response .= "𝗦𝘁𝗮𝘁𝘂𝘀 - 𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌\n";
        $response .= "━━━━━━━━━━━━━\n";
        $response .= "[ϟ] 𝗜𝗡𝗣𝗨𝗧 ⌁ {$value}\n";
        $response .= "[ϟ] 𝗦𝘁𝗮𝘁𝘂𝘀 : " . ($result['message'] ?? "Declined") . " ❌\n";
        $response .= "[ϟ] 𝗚𝗮𝘁𝗲 - API Check\n";
        $response .= "━━━━━━━━━━━━━\n";
        $response .= "[ϟ] 𝗦𝗰𝗿𝗮𝗽𝗽𝗲𝗱 𝗕𝘆 : @abinjmoffical\n";
    }

} else {

    $response .= "𝗦𝘁𝗮𝘁𝘂𝘀 - ERROR ❌\n";
    $response .= "━━━━━━━━━━━━━\n";
    $response .= "[ϟ] X Error: " . ($result['error'] ?? "Unknown error") . "\n";
}

        editMessage($chatId, $waitMsg, $response);

    }
}

function sendMessage($chatId, $text, $replyTo = null){
    global $botToken;
    $params = [
        'chat_id' => $chatId,
        'text' => $text,
        'parse_mode' => 'HTML',
    ];

if($replyTo){
    $params['reply_to_message_id'] = $replyTo;
}

$response = file_get_contents("https://api.telegram.org/bot$botToken/sendMessage?" . http_build_query($params));
$response = json_decode($response, true);

return $response['result']['message_id'] ?? null;



}


function editMessage($chatId, $messageId, $newText){
    global $botToken;
    $params = [
        'chat_id' => $chatId,
        'message_id' => $messageId,
        'text' => $newText,
        'parse_mode' => 'HTML',
    ];

   file_get_contents("https://api.telegram.org/bot$botToken/editMessageText?" . http_build_query($params));
}


