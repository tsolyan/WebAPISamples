<?php

//---- API Service: MailingReportService\EnumerateMailings 
//---- This service details all the campaign reports in an account. 
//---- Optionally a filter can be added to refine the results. In this example 
//---- we'll perfrom just a basic query to return campaigns delivered after 
//---- 22 August 2009 and before 27 August 2009.

//---- Setting some basic variables. If you need help determining your
//---- account key, username or password please contact you ReachMail account
//---- administrator or support@reachmail.com. For information on the API
//---- service URL please refer to the documentation at
//---- services.reachmail.net 
$account_key = 'account-id';
$username = 'username';
$password = 'password';
$api_service_url = 'https://services.reachmail.net/Rest/Reporting/Content/Mailings/v1/query/';

//---- For information on getting the API account id please refer to the 
//---- AdministrationService/GetCurrentUser example
$account_id = 'api-account-id';
$api_service_url = $api_service_url.$account_id;

//---- The header variable will be used in the cURL options, the request body
//---- is the body of the post that will be made to the API service URL
$header = array("Content-Type: application/xml");
$request_body = '<MailingFilter><DeliveryScheduledAfter>2009-08-22</DeliveryScheduledAfter><DeliveryScheduledBefore>2009-08-27</DeliveryScheduledBefore></MailingFilter>'; 

//---- Intialize cURL, set options and make the request
$enumerate_mailings_report_request = curl_init();
$curl_options = array(
	CURLOPT_URL => $api_service_url,
	CURLOPT_HEADER => false,
	CURLOPT_USERPWD => "$account_key\\$username:$password",
	CURLOPT_HTTPHEADER => $header, 
	CURLOPT_POST => true,
	CURLOPT_POSTFIELDS => $request_body,
	CURLOPT_RETURNTRANSFER => true 
	);
curl_setopt_array($enumerate_mailings_report_request, $curl_options);
$enumerate_mailings_report_response = curl_exec($enumerate_mailings_report_request);
curl_close($enumerate_mailings_report_request);

//---- Load the XML from the response into a parser via simplexml
$mail_report_xml = simplexml_load_string($enumerate_mailings_report_response);
$delivered = array();
$mail_names = array();
$mail_ids = array();

foreach($mail_report_xml->Mailing as $mailing){
	$delivered[] = $mailing->DeliveredDate;
	$mail_names[] = $mailing->Name;
	$mail_ids[] = $mailing->Id;
}

$mail_count = count($mail_ids);

print "\nFormat - Mail Name : Mail ID : Delivered Date\n";
for($i=0; $i<$mail_count; $i++){
	print $mail_names[$i]." : ".$mail_ids[$i]." : ".$delivered[$i]."\n";
}
print "\n";
?>
