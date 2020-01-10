import React from 'react';
import { Form, Button, Row, Col, Container} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.css';
import './sign_in.css';
export default class SignIn extends React.Component {  // export default is the class that is accessable from outside
  constructor(props) {
      super(props);
      this.state = {
          username: '',
          password: ''
      };

      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
      this.redirectToSignUp = this.redirectToSignUp.bind(this);
  }

  handleChange(event) {
      const { name, value } = event.target;
      this.setState({ [name]: value });
  }

  handleSubmit(event) {
    event.preventDefault();
    const axios = require('axios');
    axios.post(
      "http://127.0.0.1:5000/sign_in",
      this.state
    ).then(response => {
      console.log(response);
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          window.location = window.location.origin + "/" + response.data.id;
          break;
        case "failure":
          alert(response.data.payload);
          break;
        default:
          alert("Web broken. Please refresh this page.");
      }
    });
  }

  redirectToSignUp() {
      this.props.history.push("/sign_up");
  }

  render() {
    const { username, password } = this.state;
    return (
      <Container>
        <Row style={{paddingTop: '50px'}}>
          <Col lg={8}>
            <div>
              <h4>
              Issue Traking System for the software engineering
              </h4>
              <p>
              Manage your repositories and provide code stores and reviews. Each project can also have an issue tracker.
              </p>
            </div>
        </Col>
          <Col lg={4}>
          <div className="border border-black" style={{padding: "10px"}}>
            <Form onSubmit={this.handleSubmit}>
              <Form.Group controlId="formBasicUsername">
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" name="username" value={username} onChange={this.handleChange}/>
              </Form.Group>

              <Form.Group controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" name="password" value={password} onChange={this.handleChange}/>
              </Form.Group>
              <Button variant="primary" type="submit" style={{margin: "5px"}}>Login</Button>
              <Button variant="outline-dark" style={{margin: "5px"}} onClick={this.redirectToSignUp}>Sign Up</Button>
            </Form>
            </div>
          </Col>
        </Row>
      </Container>
    );
  }
}
