/**
 * Created by edx on 01-25-16.
 */
var app = angular.module('binacle', [ 'ngSanitize', 'ngCkeditor']);

app.config(function($interpolateProvider, $httpProvider){
    $interpolateProvider.startSymbol('[[')
        .endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.factory('binacleFactory', function ($http) {
    var binacle = {};
    //#############################INIT DATA###############################################
    //cargar todas las notas
    binacle.loadNotes = $http.get('/api/binnacle/pages/').success(function(data){
       binacle.notes = data;
    });

    binacle.getNotes = function (callback) {
        binacle.loadNotes.then(function () {
            callback(binacle.notes)
        })
    }

    binacle.openNote = function(note_obj, callback, error_callback){
        $http.post('/api/binnacle/notes/', note_obj).success(function (data) {
            callback(data);
        }).error(function (data, status) {
            error_callback(data, status);
        })
    };

    binacle.closeNote = function(note_id, obj_data, callback, error){
        $http.put('/api/binnacle/notes/'+note_id+'/', obj_data).success(function (data) {
            callback(data);
        }).error(function (data) {
            error(data);
        })
    };

    return binacle;
})
     
app.controller('homeCtrl', function($scope, $http, binacleFactory){
    $scope.index = 0
    $scope.editorOptions = {
        language: 'es',
        uiColor: '#CFD8DC',
        height: "200px"
    };

    $('.dimmer').toggleClass('active');
    binacleFactory.getNotes(function (data) {
        $scope.notes = data;
        for(i=0;i<data.results.length;i++)
            $scope.notes.results[i].time_since = moment().diff(data.results[i].created_at,'minutes')
        $('.dimmer').toggleClass('active');
    })

    $scope.initSelect2 = function () {
        //$("select").select2();
        //$("select").val("");
    }

    $scope.open_note = function (isValid) {
        if(isValid){
            $scope.note_model.annotations_tags = []
            if($scope.note_model.annotations)
                $scope.note_model.annotations_tags.push($scope.note_model.annotations)
            $('.dimmer').toggleClass('active');
            binacleFactory.openNote($scope.note_model, function(data){
                $('.dimmer').toggleClass('active');
                $scope.notes.results.unshift(data)
            }, function(error, status){
                console.log(error)
                console.log(status)
                if(status==406){
                    if(error.non_field_errors){
                        UIkit.notify({
                            message: '<center><b>¡Aviso!</b></center>'+ error.non_field_errors[0],
                            status: 'warning',
                            timeout: 5000,
                            pos: 'top-center'
                        });
                    }else {
                        UIkit.notify({
                            message: 'Error 406: Datos invalidos',
                            status: 'danger',
                            timeout: 5000,
                            pos: 'top-center'
                        });
                    }
                }else if(status==403){
                    UIkit.notify({
                      message : 'Error 403: '+ error.detail,
                      status  : 'danger',
                      timeout : 5000,
                      pos     : 'top-center'
                    });
                }
                else if(status==500){
                    UIkit.notify({
                      message : 'Error 500: INTERNAL SERVER ERROR',
                      status  : 'danger',
                      timeout : 5000,
                      pos     : 'top-center'
                    });
                }
                $('.dimmer').toggleClass('active');
            });
        }
    }


    $scope.close_note = function (note_id, note, keep_open) {
        $('.dimmer').toggleClass('active');
        var index = $scope.notes.results.indexOf(note[0][0])
        binacleFactory.closeNote(note_id, {'open':keep_open}, function (data) {
            $scope.notes.results[index] = data;
            $scope.notes.results[index].time_since = moment().diff($scope.notes.results[index].created_at,'minutes')
            $('.dimmer').toggleClass('active');
        }, function (error) {
            $('.dimmer').toggleClass('active');
        });
        
    }
    $scope.anotacion = {}
    $scope.write_to_note = function (Valid, note_id, note) {

        if(Valid) {
            $('.dimmer').toggleClass('active');
            var index = $scope.notes.results.indexOf(note[0][0])
            nueva_entrada = ""
            if(!note[0][0].edit)
                nueva_entrada = note[0][0].description2;

            data_edit =  {'description': note[0][0].description+" " + nueva_entrada}
            data_edit.annotations_tags = note[0][0].annotations_tags

            if(data_edit.annotations_tags.indexOf(parseInt(note[0][0].annotations)) === -1 && note[0][0].annotations)
                data_edit.annotations_tags.push(parseInt(note[0][0].annotations));

            binacleFactory.closeNote(note_id, data_edit, function (data) {
                $scope.notes.results[index] = data;
                note[0][0].description2 = ""
                note[0][0].annotations = ""
                $('.dimmer').toggleClass('active');
            }, function (error) {
                console.log(error)
                $('.dimmer').toggleClass('active');
            });

        }

    }




    $scope.navigate = function (page) {
        dep=""
        if($scope.index > 0)
            dep = $scope.index
        $http.get('/api/binnacle/pages/'+page+'&dependency='+dep).success(function(data){
            $scope.notes = data;
        });
    }

    $scope.filter_user_pos = function (dep) {
        $scope.positions = [];
        $scope.note_model.position1 = null

        $http.get('/api/accounts/users/?dependency='+dep).success(function(data){
            $scope.positions = data;
        });

    }


      $scope.filter_binnacle = function (dep) {
        $scope.index = dep
        if(dep<=0)
            dep = ""
        $http.get('/api/binnacle/pages/?dependency=' + dep).success(function (data) {
                $scope.notes = data;
                for (i = 0; i < data.results.length; i++)
                    $scope.notes.results[i].time_since = moment().diff(data.results[i].created_at, 'minutes')
            });
    }

});
