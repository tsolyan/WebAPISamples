<?php

$account_key = 'account-id';
$username = 'username';
$password = 'password';

$api_service_url = 'https://services.reachmail.net/Rest/Contacts/v1/lists/export/' . 'account-api-id' . 'list-id';

//---- Intialize cURL and set the options.

$header = array("Content-Type: application/xml");
$request_body = '<ExportParameters></ExportParameters>';

$request_body =  '
<ExportParameters>
<ExportOptions>
<Format>CharacterSeperated</Format>
<HeaderRow>true</HeaderRow>
 <CharacterSeperatedData>
<Delimiter>Comma</Delimiter>
 </CharacterSeperatedData>
<FieldMapping>

<FieldMapping>
 <DestinationFieldName>Email</DestinationFieldName>
<SourceFieldName>Email</SourceFieldName>
 </FieldMapping>

<FieldMapping>
<DestinationFieldName>Name</DestinationFieldName>
 <SourceFieldName>FullName</SourceFieldName>
</FieldMapping>

<FieldMapping>
<DestinationFieldName>OptOut</DestinationFieldName>
 <SourceFieldName>OptOut</SourceFieldName>
</FieldMapping>

<FieldMapping>
<DestinationFieldName>Other</DestinationFieldName>
 <SourceFieldName>Other</SourceFieldName>
</FieldMapping>

<FieldMapping>
<DestinationFieldName>AccountNumber</DestinationFieldName>
 <SourceFieldName>AccountNumber</SourceFieldName>
</FieldMapping>

</FieldMapping>
 </ExportOptions>
</ExportParameters>
';



//---- Intialize cURL, set options and make the request
$account_id_request = curl_init();
$curl_options = array(
        CURLOPT_URL => $api_service_url,
        CURLOPT_HEADER => false,
        CURLOPT_USERPWD => "$account_key\\$username:$password",
        CURLOPT_HTTPHEADER => $header,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $request_body,
        CURLOPT_RETURNTRANSFER => true
        );

curl_setopt_array($account_id_request, $curl_options);

$response = curl_exec($account_id_request);


preg_match("/id>(.*?)</i", $response, $matches);

if ($matches[1]) {
	$file_id = $matches[1];

} else {
	print "ERROR getting file ID\n";
	print "$response\n\n";
	exit;
}


####################################################################3


$api_service_url = 'https://services.reachmail.net/Rest/Data/' . $file_id;

$header = array("Content-Type: application/xml");

//---- Intialize cURL, set options and make the request
$account_id_request = curl_init();
$curl_options = array(
        CURLOPT_URL => $api_service_url,
        CURLOPT_HEADER => false,
        CURLOPT_USERPWD => "$account_key\\$username:$password",
        CURLOPT_HTTPHEADER => $header,
        CURLOPT_POST => false,
        CURLOPT_RETURNTRANSFER => true
        );

curl_setopt_array($account_id_request, $curl_options);

$response = curl_exec($account_id_request);
print $response;
exit;

?>
