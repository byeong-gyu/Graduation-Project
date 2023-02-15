
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewprt" content="width=device-width", initial-scale="1">
<link rel="stylesheet" href="css/bootstrap.css">
<link rel="stylesheet" href="css/custom.css">

<title>Let's go Home</title>
</head>
<body>
	<nav class="navbar navbar-default">
		<div class="navbar-header">
			<button type="button" class="navbar-toggle collapsed"
			data-toggle="collapse" data-target="#bs-example-navbar-collapse-1"
			aria-expanded="false">
			<span class="icon-bar"></span>
			<span class="icon-bar"></span>
			</button>
			<a class="navbar-brand" href="main.ejs">실종자 찾기 사이트</a>
		</div>
		<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1" aria-expanded="false">
			<ul class="nav navbar-nav navbar-right">
				<li class="dropdown">
					<a href="#" class="dropdown-toggle"
                     data-toggle="dropdown" role="button" aria-haspopup="true"
                     aria-expanded="false">메뉴<span class="caret"></span></a>
                     <ul class="dropdown-menu">
                     	<li class="active"><a href="join.ejs">회원가입</a></li>
                     	<li><a href="bbs.ejs">실종자 찾기</a></li>
					</ul>
				</li>
			</ul>
		</div>
	</nav>
<div class="container">
           <div class="col-Lg-4"></div>
           <div class="col-Lg-4"></div>          
              <div class="jumbotron" style="padding-top: 20px;">
               	<form method="POST" action="/auth/join">
               <div style="text-align : center;">
               <img src="image/main.jpg"  style="height:400px; width:1000px;"></div>
				<br><br>
                <h3 style="text-align: center;">회원가입 화면</h3>
                <div class="form-group">
                <input type="text" class="form-control" placeholder="아이디" id="userID" name="userID" maxlength="20">
                  </div>
                  <div class="form-group">
                <input type="password" class="form-control" placeholder="비밀번호" id="userPassID" name="userPassID" maxlength="20">
                  </div>
                  <div class="form-group">
                <input type="text" class="form-control" placeholder="이름" id="userName" name="userName" maxlength="20">
                  </div>
                  <div class="form-group" style="text-align: center;">
               			<div class="btn-group" data-toggle="buttons">
               				<label class="btn btn-primary active">
               					<input type="radio" id="userGender" name="userGender" autocomplete="off" value="남자" checked>남자
               				</label>
               					<label class="btn btn-primary">
               					<input type="radio" id="userGender" name="userGender" autocomplete="off" value="여자" checked>여자
               				</label>
               			</div>
                  </div>
                    <div class="form-group">
                <input type="email" class="form-control" placeholder="이메일" id="userEmail" name="userEmail" maxlength="20">
                  </div>
                    <div class="form-group">
                <input type="text" class="form-control" placeholder="코드" id="userCode" name="userCode" maxlength="20">
                  </div>
                   <input type="submit" class="btn btn-primary form-control" value="회원가입">
                  </form>
              </div>               
          </div>	
	<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
	<script src="js/bootstrap.js"></script>
</body>
</html>