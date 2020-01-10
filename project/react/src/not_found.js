import React from 'react';
import { Form, Button, Row, Col, Container} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.css';
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
          <Col lg={12}>
            <div>
              <h1>
              404
              </h1>
              <h4>
              Page Not Found
              </h4>
              <p>
              Make sure the address is correct and the page hasn't moved.
              </p>
            </div>
            </Col>
        </Row>
      </Container>
    );
  }
}
