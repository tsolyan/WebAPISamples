<?php

$account_key = $argv[1];
$username = $argv[2]; 
$password = escapeshellarg($argv[3]);
//--$file = $argv[4]; 
$api_aid_service_url = 'https://services.reachmail.net/Rest/Administration/v1/users/current';

echo "$account_key\\$username:$password";

//---- Intialize cURL and set the options.
$account_id_request = curl_init();
$curl_options = array(
	CURLOPT_URL => $api_aid_service_url,
	CURLOPT_HEADER => false,
	CURLOPT_USERPWD => "$account_key\\$username:$password",
	CURLOPT_RETURNTRANSFER => true
	);
curl_setopt_array($account_id_request, $curl_options);

$response = curl_exec($account_id_request);

//---- Load the XML from the response into the simplexml parser and get the 
//---- account id.
$xml = simplexml_load_string($response);

$account_id = $xml->AccountId;

print "\n".$account_id."\n\n";
?>
