<?php

include('file_class.php');
include('cache_class.php');

class templateUtil {
	public static function render($template,$arg=array()){
		$templateContent=fileUtil::read('templates/'.$template.'.sml');
		$cache=templateUtil::shade($templateContent,$arg);
		echo $cache;
	}
	public static  function shade($templateContent,$arg=array()){
		$templateContent=templateUtil::checkImage($templateContent,$arg);
		$templateContent=templateUtil::checkConfig($templateContent);
		$templateContent=templateUtil::checkVar($templateContent,$arg);
		foreach ($arg as $key => $value) {
			$templateContent=str_replace('{{'.$key.'}}', $value, $templateContent);
		}
		return $templateContent;
	}

	public static function checkImage($templateContent,$arg=array()){
		foreach ($arg as $key => $value) {
			if(preg_match('/gopher|file/i', $value)){
				$templateContent=str_replace('{{img:'.$key.'}}', '', $templateContent);
			}
			if(stripos($templateContent, '{{img:'.$key.'}}')){
				$encode='';
				if(file_exists(__DIR__.'/../cache/'.md5($value))){
					$encode=file_get_contents(__DIR__.'/../cache/'.md5($value));
				}else{
					$ch=curl_init($value);
					curl_setopt($ch, CURLOPT_HEADER, 0);
					curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
					$result=curl_exec($ch);
					curl_close($ch);
					$ret=chunk_split(base64_encode($result));
					$encode = 'data:image/jpg/png/gif;base64,' . $ret;
					file_put_contents(__DIR__.'/../cache/'.md5($value), $encode);
				}
				$templateContent=str_replace('{{img:'.$key.'}}', $encode, $templateContent);
			}
			
		}
		return $templateContent;
	}
	public static function checkConfig($templateContent){
		$config = unserialize(file_get_contents(__DIR__.'/../config/settings'));
		foreach ($config as $key => $value) {
			if(stripos($templateContent, '{{config:'.$key.'}}')){
				$templateContent=str_replace('{{config:'.$key.'}}', $value, $templateContent);
			}
			
		}
		return $templateContent;
	}

	public static function checkVar($templateContent,$arg){
		$db=new db();
		foreach ($arg as $key => $value) {
			if(stripos($templateContent, '{{var:'.$key.'}}')){
				if(!preg_match('/\(|\[|\`|\'|\"|\+|nginx|\)|\]|include|data|text|filter|input|file|require|GET|POST|COOKIE|SESSION|file/i', $value)){
					eval('$v='.$value.';');
					$templateContent=str_replace('{{var:'.$key.'}}', $v, $templateContent);
				}
				
			}
		}
		return $templateContent;
	}


}



