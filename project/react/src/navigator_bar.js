import React from 'react';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.css';
import { Global } from './global.js'
export default class NavigatorBar extends React.Component {  // export default is the class that is accessable from outside
  constructor(props) {
    super(props);
    this.state = {
      username: ""
    };

    const axios = require('axios');
    axios.post(
      Global.backend_host + "/user/check"
    ).then(response => {
      if (response.data.info === "success"){
        this.setState({username: response.data.payload});
      }else if (response.data.info === "redirect"){
        if(window.location.pathname !== response.data.location){
          this.setState({username: ""});
          window.location = response.data.location;
        }
      }
    });
  }
  signOut() {
    const axios = require('axios');
    axios.post(
      "http://127.0.0.1:5000/sign_out"
    ).then(response => {
      window.location = "/sign_in";
    });
  }
  signIn() {
    window.location = "/sign_in";
  }
  render() {
    return (
      <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        <Navbar.Brand>I.T.S</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link href={"/" + this.state.username + "/projects"}>Projects</Nav.Link>
          </Nav>
          <Nav>
            <Nav.Link eventKey={2} href={"/" + this.state.username}>
              {this.state.username !== "" ? "Hello, " + this.state.username : ""}
            </Nav.Link>
            {this.state.username !== "" ?
              <Nav.Link onClick={this.signOut}>Sign out</Nav.Link> :
              <Nav.Link onClick={this.signIn}>Sign in</Nav.Link>
            }
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      // code in red brackets are react js code
    );
  }
}
/*<Nav.Link href="#pricing">Pricing</Nav.Link>
<NavDropdown title="Dropdown" id="collasible-nav-dropdown">
  <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
  <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
  <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
  <NavDropdown.Divider />
  <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
</NavDropdown>*/
