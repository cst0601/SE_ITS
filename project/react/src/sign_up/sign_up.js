import React from 'react';
import { Form, Button, Row, Col, Container} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.css';
import { Global } from '../global.js'
export default class SignUp extends React.Component {  // export default is the class that is accessable from outside
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      name: "",
      email: "",
      password: ""
    };

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);

  }

  handleSubmit(event) {
    event.preventDefault();
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/sign_up",
      this.state
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          alert(response.data.payload);
          this.props.history.push("/sign_in");
          break;
        case "failure":
          alert(response.data.payload);
          break;
        default:
          alert("Web broken. Please refresh this page.");
      }
    });
  }

  handleChange(event) {
    const { name, value } = event.target;
    this.setState({ [name]: value });   /* <--- {} is for JSON :) */
  }

  render() {
    return (
      <Container>
        <Row style={{paddingTop: '50px'}}>
          <Col lg={12}>
            <h2>Create your account</h2>
            <Form onSubmit={this.handleSubmit}>
              <Form.Group controlId="formGridUsername">
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" name="username" required value={this.state.username} pattern="[a-zA-Z0-9]{8,16}" onChange={this.handleChange} />
                <Form.Text className="text-muted">
                  Make sure it's at least 8 characters and at most 16 characters.
                </Form.Text>
              </Form.Group>
              <Form.Group controlId="formGridName">
                <Form.Label>Name</Form.Label>
                <Form.Control type="text" name="name" required value={this.state.name} onChange={this.handleChange}/>
              </Form.Group>
              <Form.Group controlId="formGridEmail">
                <Form.Label>Email</Form.Label>
                <Form.Control type="email" name="email" required value={this.state.email} onChange={this.handleChange} />
              </Form.Group>
              <Form.Group controlId="formGridPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" name="password" required value={this.state.password} onChange={this.handleChange} />
                <Form.Text className="text-muted">
                  Make sure it's at least 8 characters and at most 16 characters.
                </Form.Text>
              </Form.Group>
              <Button variant="primary" type="submit">
                Register
              </Button>
              <Form.Text className="text-muted">
                By creating an account, you agree to the Terms of Service.
              </Form.Text>
            </Form>
          </Col>
        </Row>
      </Container>
    );
  }
}
