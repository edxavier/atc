/**
 * Created by edx on 01-25-16.
 */
var app = angular.module('binacle', ['ngSanitize']);

app.config(function($interpolateProvider, $httpProvider){
    $interpolateProvider.startSymbol('[[')
        .endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

     
app.controller('searchCtrl', function($scope, $http){

    $scope.filter_notes = function (isValid) {
        if(isValid){
            $('.dimmer').toggleClass('active');
            var filter_str = "?min_date="+$scope.search.initDate+"&max_date="+$scope.search.endDate
            if($scope.search.turn)
                filter_str += "&turn="+ $scope.search.turn
            if($scope.search.ucs)
                filter_str += "&ucs="+ $scope.search.ucs
            if($scope.search.position1)
                filter_str += "&position1="+ $scope.search.position1
            if($scope.search.position2)
                filter_str += "&position2="+ $scope.search.position2
            if($scope.search.description)
                filter_str += "&description="+ $scope.search.description
            if($scope.search.annotations)
                filter_str += "&annotations_tags="+ $scope.search.annotations

            $http.get('/api/binnacle/notes/'+filter_str).success(function(data){
                $scope.notes = data;
                UIkit.notify({
                      message : 'Resultados obtenidos: ' +  data.length,
                      status  : 'info',
                      timeout : 5000,
                      pos     : 'top-center'
                  });
                $('.dimmer').toggleClass('active');
            }, function(error){
                console.log(error)
                UIkit.notify({
                      message : 'Error',
                      status  : 'error',
                      timeout : 5000,
                      pos     : 'top-center'
                  });
                $('.dimmer').toggleClass('active');
            });
        }
    }
    
    $scope.export_all = function () {
        notes_ids =  new Array()
        $scope.notes.forEach(function(entry) {
            notes_ids.push(entry.id)
        });
        json = JSON.stringify(notes_ids);
        var win = window.open('/binnacle/report/notes/?vars='+json, '_blank');
        win.focus();

    }

    $scope.export_selected = function () {
        notes_ids =  new Array()
        $scope.notes.forEach(function(entry) {
            if(entry.selected)
                notes_ids.push(entry.id)
        });
        if(notes_ids.length>0) {
            json = JSON.stringify(notes_ids);
            var win = window.open('/binnacle/report/notes/?vars=' + json, '_blank');
            win.focus();
        }else{
            UIkit.notify({
                      message : 'No ha seleccionado ninguna de las notas',
                      status  : 'warning',
                      timeout : 0,
                      pos     : 'top-center'
            });
        }

    }
    
});
