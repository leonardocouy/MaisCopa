    var app = angular.module('myapp',['ui.router', 'chieffancypants.loadingBar']);
    // INICIALIZANDO MINHA "APLICAÇÃO" NO ANGULAR, COM AS DEPENDENCIAS DO "UI.ROUTER" & "LOADING BAR"
    //
    // O UI.ROUTER É UM FRAMEWORK DE ROTEAMENTO DO ANGULARJS QUE É UM JEITO MAIS EFICIENTE E ORGANIZADO
    // DE ROTEAR DO QUE O METODO ORIGINAL QUE VEM DO ANGULARJS (QUE POSSUI LIMITAÇÕES E REGRAS)
    //
    // O chieffancypants.loadingBar é uma barra de progresso que surge automaticamente toda vez que ocorre
    // uma requisição(retorno de resposta).
    //

    app.config( // CONFIGURAÇÕES
            function ($interpolateProvider, $stateProvider, $locationProvider) {
                $interpolateProvider.startSymbol('{_').endSymbol('_}'); // MUDANDO O SIMBOLOS DO ANGULAR, POIS O JINJA UTILIZA OS MESMOS.
                $locationProvider.html5Mode(true); // SE TIVER NO MODO FALSE, ADICIONA O '#'
                $stateProvider  // COMEÇANDO O ROTEAMENTO COM A DEPENDENCIA UI.ROUTER USANDO A FUNÇÃO stateProvider
                .state('route_index',{  // ROTEANDO A PAGINA PRINCIPAL.
                url: "/",
                controller: CopaController // CONTROLADOR QUE SERÁ UTILIZADO NA PAGINA PRINCIPAL
                })

                .state('route_info',{ // ROTEANDO A PAGINA DE INFORMAÇÕES
                url: "/infos",
                templateUrl: "/infos"
                })

            }); // FIM CONFIGS


    app.run(function($rootScope){ // RODANDO NA APLICAÇÃO PRINCIPAL UMA VARIAVEL GLOBAL NO ESCOPO GLOBAL.
            $rootScope.info = []; // VARIAVEL GLOBAL INFO, ONDE FICARÁ A INFORMAÇÃO ARMAZENADA, PARA SER PASSADO PARA PAGINA INFO.
    });

    function CopaController($scope, $http, $window, $rootScope){ // INICIALIZANDO MEU CONTROLADOR COPA COM SUAS FUNÇÕES.
        $scope.infos = [];            ////////////////////////////////////////////
        $scope.listaCidades = [];     // O $scope, é o contrario do rootScope,
        $scope.listaTemas = [];       // ele só pode ser usado localmente.(locais)
        $scope.pesquisa = [{}];       ////////////////////////////////////////////
        $scope.showHeader = false;

        $scope.listarTemas = function(){
            $http.get('../../infos/listar_temas').success(function(listaDeTemas){ // ACESSANDO E PEGANDO(GET) O CONTEUDO DO SITE LISTADO E COLOCANDO NO listaDeTemas
                $scope.listaTemas = listaDeTemas; // A variavel local "listaTemas" tá recebendo o conteudo pego de listaDeTemas
            });
        };

        $scope.listarCidades = function(){
            $http.get('../../infos/listar_cidades').success(function(listaDeCidade){
                $scope.listaCidades = listaDeCidade;
            });
        };

        $scope.listarRegistros = function(cidade,tema){
           $http.get('../../infos/buscar_infos/'+ cidade + '/' + tema).success(function(listaDeInfos){
              $scope.infos = listaDeInfos;

               if ($scope.infos == ''){
                  $window.alert('Não possui registros sobre esse tema nesta cidade.\nBusque por outro tema!'); // CASO NÃO POSSUA INFORMAÇÕES DA CIDADE E DO TEMA                                                                                               // APARECE UMA JANELA PARA O USUARIO ALERTANDO.
                  $scope.showHeader = false;
               }
               else{
                   $scope.showHeader = true;
               }

           });
        };


        $scope.listarInfos = function(cod){
           $http.get('../../infos/listar_info/'+ cod).success(function(listaDeTudo){
           $rootScope.info = listaDeTudo;
           });
        };

    }

