
<?php


session_start();
include('render/render_class.php');
include('render/db_class.php');


$action=$_GET['action'];


if(!isset($action)){
	if(isset($_COOKIE['user'])){
		$c=$_COOKIE['user'];
		if(preg_match('/\:|\,/', $c)){
			$user=unserialize($c);
		}
		if($user){
			templateUtil::render('index');
		}else{
			header('location:index.php?action=login');
		}
	}else{
		header('location:index.php?action=login');
	}
	die();	
}

switch ($action) {
	case 'check':
		$username=$_POST['username'];
		$password=$_POST['password'];
		if(!preg_match('/file|innodb|sys|mysql/i', $username)){
			$sql = "select username,nickname from user where username = '".$username."' and password='".md5($password)."' order by id limit 1";
			$db=new db();
			$user=$db->select_one_array($sql);
		}
		if($user){
			$_SESSION['user']=$user;
			header('location:index.php?action=index');
		}else{
			templateUtil::render('error');
		}
		break;
	case 'clear':
		system('rm -rf cache/*');
		die('cache clear');
		break;
	case 'login':
		templateUtil::render($action);
		break;
	case 'index':
		$user=$_SESSION['user'];
		if($user){
			templateUtil::render('index',$user);
		}else{
			header('location:index.php?action=login');
		}
		break;
	case 'view':
		$user=$_SESSION['user'];
		if($user){
			templateUtil::render($_GET['page'],$user);
		}else{
			header('location:index.php?action=login');
		}
		break;
	case 'logout':
		session_destroy();
		header('location:index.php?action=login');
		break;
	default:
		templateUtil::render($action);
		break;
}

