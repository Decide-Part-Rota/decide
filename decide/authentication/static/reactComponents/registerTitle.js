"use strict";

const create = React.createElement;

class Title extends React.Component {
  render() {
    return create("body",{}, create("h2",{className:"Title"},"Sign Up"));}
    
}

const domContainer = document.querySelector("#title");
const root = ReactDOM.createRoot(domContainer);
root.render(create(Title));
