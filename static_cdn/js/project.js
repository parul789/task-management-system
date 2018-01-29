var project=angular.module("project",[]);
app.controller("create",["$scope","$http",function($scope,$http){
	$scope.title="";
	$scope.start_date="";
	$scope.stage="";
	$scope.end_date="";
	$scope.create=function(){
	console.log('inside create project');
	$http({
		method:'POST',
		url:'http://127.0.0.1:8000/project/create/',
		headers:{
			'Content-Type':'application/json',
			'Authorization':Token 6a4eefd97f0452cf39ae64b68ab0f55c69d1be5b
		},
		data: {"title":$scope.title,
	            "start_date":$scope.start_date,
	            "stage":$scope.stage,
	            "end_date":$scope.end_date
	            }
	}).then(function successCallback(response){
		console.log(response);
	},function errorcallback(response){
		console.log(response);
	});
    };
}])
