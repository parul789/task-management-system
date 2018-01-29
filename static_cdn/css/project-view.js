var project = angular.module ('project',[]);
project.controller("project-create",function($scope){
	$scope.projects = [];
	$scope.addRow=function(){
		$scope.projects.push({
			'title':$scope.title
		});
		$scope.title="";
	};
	
)};