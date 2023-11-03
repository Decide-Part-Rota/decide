"use strict";

const create = React.createElement;
const datos = document.getElementById("hide").value;

const nombreBueno = voting.name
const id = voting.id
const desc = voting.desc

//const view = [];
//const keys = Object.keys(dicc);

//const id = keys[0];
//const lista = dicc[0];
//const nombre = lista[1];
//const desc = lista[2];


  //view.push(aux)


class Contenedor extends React.Component {
  
    render() {
        return create("div", {className : "card"},
        create("div", {className : "face face1"},
        create("div", {className : "content"},
        create("h1", {className : "name"},id + "  -  " + nombreBueno,))),
        create("div", {className : "face face2"},
        create("div", {className : "content"},
        create("h5",{className : "nombre"},desc))));
  
    }
  }

const domContainer = document.querySelector('#caja');
const root = ReactDOM.createRoot(domContainer);
root.render(create(Contenedor));