<?php
    include ('connect.php');
?>
<?php

    if (isset($_POST['submit']) && !empty($_POST['ssid']) && !empty($_POST['mac'])) 
    {
        $ssid = mysql_real_escape_string($_POST['ssid']);
        $mac = mysql_real_escape_string($_POST['mac']);
        
        $search = mysql_query("SELECT * FROM bus_table WHERE ssid='".$ssid."' AND mac='".$mac."'") or die(mysql_error()); 
        $match  = mysql_num_rows($search);        

        if($match == 1 ){
                // We have a match, update the placed
            echo '<script>alert("Entry already done");</script>';                        
        }            
        else{
                // No match -> invalid url or account has already been activated.
            $query = "INSERT INTO bus_table(ssid,mac) VALUES('$ssid','$mac')";
            $check=mysql_query($query) or die(mysql_error());           
            echo '<script>alert("Done");</script>';                        
        }        
    }
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">    
    <meta name="title" content="Bus Data">
    <meta name="author" content="Inderjeet Vashista">
    <title>Bus Data</title>
    <link href="./css/bootstrap-theme.min.css"  rel="stylesheet" type="text/css">
    <link href="./css/bootstrap.min.css" rel="stylesheet" type="text/css" />        
</head>
<body>
    <div class="container">    
        <div id="loginbox" style="margin-top:50px;" class="mainbox col-md-6 col-md-offset-3 col-sm-8 col-sm-offset-2">                
            <div class="panel panel-info" >
                <div class="panel-heading">
                        <div class="panel-title">Bus Data</div>
                </div>             
                    <div style="padding-top:30px" class="panel-body" >
                        <div style="display:none" id="login-alert" class="alert alert-danger col-sm-12"></div>
                        <form id="loginform" class="form-horizontal" role="form" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>" method="post" autocomplete="on">
                                    
                            <div style="margin-bottom: 25px" class="input-group">
                                <span class="input-group-addon"><i class="glyphicon glyphicon-user"></i></span>
                                <input type="text" class="form-control" name="ssid" placeholder="Enter SSID" autofocus required>                                        
                            </div>
                                
                            <div style="margin-bottom: 25px" class="input-group">
                                <span class="input-group-addon"><i class="glyphicon glyphicon-lock"></i></span>
                                <input type="text" class="form-control" name="mac" placeholder="Enter MAC Address">
                            </div>
                                
                                <div style="margin-top:10px" class="form-group">
                                    <!-- Button -->

                                    <div class="col-sm-12 controls">
                                        <button type="submit" class="btn btn-success btn-sm" name="submit">Submit</button>          
<!--                                      <a id="btn-login" href="#" class="btn btn-success">Login  </a>-->
        <!--                              <a id="btn-fblogin" href="#" class="btn btn-primary">Login with Facebook</a>-->

                                    </div>
                                </div>

                        </form>     
                    </div>                     
                </div>  
        </div>    
    </div>    
</body>
</html>
