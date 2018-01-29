var project = angular.module('project',['ngRoute'], function($locationProvider){
    $locationProvider.html5Mode({
	  enabled: true,
	  requireBase: false
	});
});

project.config(["$interpolateProvider", function($interpolateProvider){
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');	
}]);

project.run(['$rootScope','$route','$location','$window', '$http',
    function ($rootScope,$route,$location ,$window, $http) {
  		$rootScope.$on('$locationChangeStart', function (event, next, current) {
            // redirect to login page if not logged in
            var authdata = $window.localStorage.getItem("authData");
            var authemail = $window.localStorage.getItem("authemail");
            console.log($location.path());
            
            if ($location.path()!== '/login/' && authdata==null)  {
            	console.log('in');
                $window.location.href = '/login/';
            }
            

        });
    }]);

project.controller("projectcreateController",["$scope", "$route","$location","$http", "$window",function($scope,$route, $location,$http, $window){
	$scope.data = {};
	$scope.order ;
	$scope.taskdata = {};
	$scope.processdata ={};
	$scope.userdata={};
	$scope.s= false;
	$scope.q = null;
	var authdata = $window.localStorage.getItem("authData");

	$scope.listProjects = function(){
		console.log('inside PROJECT LIST function');
		if ($scope.q)
			var url = '/project/?q='+ $scope.q
		else
			var url = '/project/'
		$http({
			method:'GET',
			url: url,
		    headers:{
				'Content-Type':'application/json',
				'Authorization': authdata,
		},
		}).then(function successCallback(response){
		console.log(response);
		$scope.projects = response.data;
		var authemailid = $window.localStorage.getItem("authemail");
		$scope.welcmsg = authemailid;
		$window.localStorage.removeItem("query");
        },function errorcallback(response){
		console.log(response);
	});
    };

    $scope.removeLocalStorage =  function(){
    	console.log('inside removeLocalStorage function');
    	console.log(q);
		
    };

	$scope.projectCreate = function(){
		console.log('in PROJECT CREATE function');
		$http({
			method:'POST',
		    url:'/project/create/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization': authdata
		},
		data: $scope.data,
		}).then(function successCallback(response){
		console.log(response);
		$scope.listProjects();
 		$window.location.reload();
        },function errorcallback(response){
		console.log("error")
		console.log(response);
		$window.alert("project not created");
		$window.location.reload();
	});
	};

	$scope.stageDetails = function(id){
		console.log('in stage details function');
		console.log(id);
		$http({
			method:'GET',
		    url:'/stage/detail/'+ id + '',
		    headers:{
				'Content-Type':'application/json',
				'Authorization': authdata
		},
		}).then(function successCallback(response){
		console.log(response);
		$scope.stg = response.data.entry;
 		//$window.location.reload();
        },function errorcallback(response){
		console.log("error")
		console.log(response);
		$window.alert("stageDetails not called");
		$window.location.reload();
	});
	};

	$scope.getstage = function(){
		var d = $window.localStorage.getItem("projct_stage");
		$scope.stageDetails(d);
	};

	$scope.bringStage =  function(){
		console.log('inside BRING stage function');
		$http({
			method:'GET',
		    url:'/stage/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		}).then(function successCallback(response){
		console.log(response);
		$scope.stage = response.data;
		},function errorcallback(response){
		console.log(response);
	});
    };

	$scope.projectUpdate = function(id){
		console.log('inside project update function');
		$http({
			method:'PUT',
		    url:'/project/update/'+id+'/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		    data:$scope.data,
		}).then(function successCallback(response){
		console.log(response);
		//$scope.stage = response.data;
		$scope.data.stage = response.data.stage;
		$window.alert("project updated successfully");
		$window.location.reload();
		},function errorcallback(response){
		console.log(response);
		console.log("update");
		$window.alert("error in updating the process");
		$window.location.reload();
	});
    };

	$scope.projectDetail =  function(id){
		console.log('projet detail id',id);
		$http({
			method:'GET',
		    url:'/project/detail/'+id+'/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		}).then(function successCallback(response){
			$scope.project_obj = response.data;
			$scope.data.stage = response.data.stage;
			console.log(response.data.stage);
			//$scope.stageDetails(response.data.stage);
			console.log(response);
        },function errorcallback(response){
			console.log(response);
	});
	};

	$scope.projectDelete = function(id){
		console.log('inside PROJECT DELETE function');
		$http({
			method:'DELETE',
		    url:'/project/delete/'+id,
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		}).then(function successCallback(response){
		$scope.listProjects();
		console.log(response);
        $window.location.reload();
		$window.alert("project deleted successfully");
		},function errorcallback(response){
		console.log(response);
		console.log("delete");
		$window.alert("Error in deleting the project");
		$window.location.reload();
	});
    };

	$scope.stageCreate = function(){
		console.log('in STAGE CREATE function');
		$http({
			method:'POST',
		    url:'/stage/create/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		data:$scope.data,
		}).then(function successCallback(response){
		console.log(response);
		$window.alert("new stage created! Now update the project");
		$window.location.reload();
		},function errorcallback(response){
		console.log("error")
		console.log(response);
		$window.alert("Error in creating new stage.");
		$window.location.reload();
	});
	};

	$scope.redirectToNext = function (id,title) {
        console.log('i m in');
   		console.log(id,title);
   		$window.localStorage.setItem("project_id", id);
   		$window.localStorage.setItem("projct_title",title);
   		$window.location.replace('/processes/');
    };

/* process operations */
    $scope.processCreate = function(){
		console.log('in process create');
		$http({
			method:'POST',
		    url:'/process/create/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		data:$scope.processdata,
		}).then(function successCallback(response){
		console.log(response);
		$scope.process =response.data;
		$scope.processList($scope.process.project);
		$window.alert("Process added successfully!");
		$window.location.reload();
		},function errorcallback(response){
		console.log("error")
		console.log(response);
		$window.alert('ERROR!it may be because you are not entering unique priority.');
		$window.location.reload();
	});
	};
    
    $scope.processDelete = function(id){
    	console.log('inside process delete');
    	$http({
			method:'DELETE',
		    url:'/process/delete/'+id+'/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		}).then(function successCallback(response){
		console.log(response);
		$window.alert("Process deleted successfully!");
		$window.location.reload();
		},function errorcallback(response){
		console.log("error")
		console.log(response);
		$window.alert("Error in deleting the process");
    });
    };

    $scope.processUpdate= function(id){
    	console.log('inside process update');
    	$http({
			method:'PUT',
		    url:'/process/update/'+id+'/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		data:$scope.processdata,
		}).then(function successCallback(response){
		console.log(response);
		$window.alert("Process updated successfully!");
		$window.location.reload();
		},function errorcallback(response){
		console.log("error")
		console.log(response);
		$window.alert("Error in updating the process");
    });
    };

    $scope.processDetail= function(id){
    	console.log('inside process detail');
    	$http({
			method:'GET',
		    url:'/process/detail/'+id+'/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		data:$scope.data,
		}).then(function successCallback(response){
			$scope.processdata.title=response.data.title;
			$scope.processdata.priority=response.data.priority;
		console.log(response);
		},function errorcallback(response){
		console.log("error")
		console.log(response);
		$window.alert("Error in updating the process");
    });
    };

    $scope.processList= function(){
    	console.log('inside process list');
        var id = $window.localStorage.getItem("project_id");
        $scope.processdata.project= id;
        $http({
			method:'GET',
		    url:'/project/detail/'+id+'/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization': authdata
		},
		}).then(function successCallback(response){
		console.log(response);
		$scope.pj_obj = response.data;
		var authemailid = $window.localStorage.getItem("authemail");
		$scope.welcmsg = authemailid;
		var ttl = $window.localStorage.getItem("projct_title");
        $scope.projecttl=ttl;
		},function errorcallback(response){
		console.log("error")
		console.log(response);
    });
    };

/* task operations */

    $scope.taskCreate = function(){
		console.log('in task create');
		$http({
			method:'POST',
		    url:'/task/create/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization': authdata,
		},
		data:$scope.taskdata,
		}).then(function successCallback(response){	
		console.log(response);
		$scope.task =response.data;
		$window.alert("task created successfully");
		$window.location.reload();
		},function errorcallback(response){
		console.log("error")
		console.log(response);
		$window.alert("ERROR! it may be because you are not entering unique order.");
		$window.location.reload();
	});
	};

    $scope.taskDelete = function(id){
    	console.log('inside task delete');
    	$http({
			method:'DELETE',
		    url:'/task/delete/'+id+'/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		}).then(function successCallback(response){
		console.log(response);
		$window.alert("Task deleted successfully!");
		$window.location.reload();
		},function errorcallback(response){
		console.log("error")
		console.log(response);
		$window.alert("Error in deleting the task");
    });
    };

    $scope.taskUpdate= function(id){
    	console.log('inside task update');
    	$http({
			method:'PUT',
		    url:'/task/update/'+id+'/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		    data:$scope.taskdata,
		}).then(function successCallback(response){
		console.log(response);
		$window.alert("Task updated successfully!");
		$window.location.reload();
		},function errorcallback(response){
		console.log("error");
		console.log(response);
		$window.alert("Error in updating the task");
		$window.location.reload();
    });
    };

    $scope.taskDetail= function(id){
    	console.log('inside task detail');
    	$http({
			method:'GET',
		    url:'/task/detail/'+id+'/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		}).then(function successCallback(response){
		console.log(response);
		$scope.taskdata.status = response.data.status;
		$scope.usernames =response.data.user_assignedto;
		$scope.creator = response.data.user_createdby;
		console.log($scope.usernames);
		},function errorcallback(response){
		console.log("error")
		console.log(response);
    });
    };

    $scope.taskList= function(id){
    	console.log('inside task update');
    	$http({
			method:'GET',
		    url:'/task/detail/'+id+'/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		}).then(function successCallback(response){
		console.log(response);
		$scope.pj_obj = response.data;
		},function errorcallback(response){
		console.log("error")
		console.log(response);
    });
    };

    $scope.sendsignal= function(order){
    	console.log('inside task sendsignal',order);
    	$http({
			method:'PUT',
		    url:'/task/status/update/'+order+'/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		data:{
			'status':"InReview"
		},
		}).then(function successCallback(response){
		console.log(response);
		$window.alert("alert sent!!");
		$window.location.reload();
		},function errorcallback(response){
		console.log("error")
		console.log(response);
		$window.alert("alert not sent!!");
		$window.location.reload();
    });
    }; 

/* TASK ID PASSING */

    $scope.pass=function(id){
    	$scope.passid=id;
    	console.log($scope.passid);
    	
    }; 

    $scope.passorderid = function(num){
    	$scope.sendsignal(num);
    };

    $scope.UserList = function(){
    	console.log('inside user list');
    	$http({
			method:'GET',
		    url:'/user/list/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		}).then(function successCallback(response){
		console.log(response);
		$scope.users = response.data;
		},function errorcallback(response){
		console.log("error")
		console.log(response);
    });
    };

	$scope.signin = function(){
    	console.log('inside user login');
    	$http({
			method:'POST',
		    url:'/user/login/',
		    headers:{
				'Content-Type':'application/json',
		},
			data:$scope.userdata,
		}).then(function successCallback(response){
		console.log(response);
		$window.localStorage.setItem("authData",response.data.token);
		$window.localStorage.setItem("authemail",response.data.email);
		var aut = $window.localStorage.getItem("authData");
		if (response.data.token== undefined){
            	console.log("rem");
            	$window.localStorage.removeItem("authData");
            }
		$window.location.replace ('/projects/');
		},function errorcallback(response){
		console.log("error")
		$window.alert("Login Again");
		$window.location.replace ('/login/');
		console.log(response);
    });
    };

    $scope.signout = function(){
    	console.log('inside user logout');
    	$http({
			method:'POST',
		    url:'/user/logout/',
		    headers:{
				'Content-Type':'application/json',
				'Authorization':authdata
		},
		}).then(function successCallback(response){
		console.log(response);
		$window.localStorage.removeItem("authData");
		$window.location.replace ('/login/');
		},function errorcallback(response){
		console.log("error")
		console.log(response);
    });
    }; 

    $scope.back = function(){
       $window.location.replace ('/projects/'); 
    };

    $scope.passprocessId = function(id){
    	console.log("inside passprocessid",id);
    	$window.localStorage.setItem("process_id",id);
    };

    $scope.getprocessID = function(){
    	console.log("inside getprocessid");
    	var j = $window.localStorage.getItem("process_id");
		$scope.taskdata.process = j;
		console.log($scope.taskdata.process);
    };

    $scope.setassignedusers = function(users){
    	console.log('inside setassignedusers function');
    	console.log(users);
    	$scope.assignedusers = users;
    	$scope.AssignedUserList($scope.assignedusers);
    };           
}]);








































































 