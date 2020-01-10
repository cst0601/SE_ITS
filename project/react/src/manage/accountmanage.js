import React from 'react';
import { Form, Row, Col, Container, Table, ListGroup, Modal, Button, Badge } from 'react-bootstrap'
import { Global } from '../global.js'
import 'bootstrap/dist/css/bootstrap.css';

export default class AccountManage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      show: false,
      username: "",
      project_name: "",
      users: [],
      new_user_name: "",
      new_user_role: "user",
      new_username: "",
      new_name: "",
      new_email: "",
      new_password: "",
      new_role: "user"
    };
    this.username = this.props.match.params.username;
    this.project_name = this.props.match.params.project_name;
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/user/list",
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          this.setState({ users: response.data.payload});
          break;
        case "failure":
          alert(response.data.payload);
          break;
        default:
          alert("Web broken. Please refresh this page.");
      }
    });

    this.handleClose = this.handleClose.bind(this);
    this.handleShow = this.handleShow.bind(this);
    this.handleSelectNewRole = this.handleSelectNewRole.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.updateRole = this.updateRole.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleClose() {this.setState({ show: false, new_user_name: "", new_user_role: "user" });}
  handleShow() {this.setState({ show: true });}
  updateRole(event, username) {
    var role = event.target.value;
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/user/update_role",
      {
        selected_username: username,
        role: role
      }
      ).then(response => {
        switch(response.data.info) {
          case "redirect":
            window.location = window.location.origin + response.data.location;
            break;
          case "success":
            this.setState({ users: response.data.payload});
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

  handleSelectNewRole(event) {
    this.setState({ new_role: event.target.value });
  }

  handleSubmit(event) {
    event.preventDefault();
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/user/create_account",
      {
        username: this.state.new_username,
        name: this.state.new_name,
        email: this.state.new_email,
        password: this.state.new_password,
        role: this.state.new_role
      }
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          this.setState({ users: response.data.payload});
          break;
        case "failure":
          alert(response.data.payload);
          break;
        default:
          alert("Web broken. Please refresh this page.");
      }
    });
    this.handleClose();
  }

  directToProfile(username){
    this.props.history.push("/" + username);
  }

  render(){
      return(
          <Container>
              <Row style={{marginTop:"20px"}}>
                  <Col>
                      <h2>Account Management</h2>
                        <Button id="button-add" variant="primary" onClick={this.handleShow}>
                          Create Account
                        </Button>
                      <p>Do ⌘F to search for specific user or attributes :)</p>

                        <Table striped bordered hover style={{marginTop:"20px"}}>
                            <thead>
                                <tr>
                                  <th>User Name</th>
                                  <th>E-mail</th>
                                  <th>Role</th>
                                </tr>
                            </thead>
                            <tbody>
                                {this.state.users.map(user => (
                                    <tr>
                                      <td onClick={() => this.directToProfile(user.username)}>{user.name}</td>
                                      <td>{user.email}</td>
                                      <td>
                                        <Form.Control as="select" value={user.role} onChange={(event) => this.updateRole(event, user.username)} key={user.username}>
                                          <option>user</option>
                                          <option>manager</option>
                                        </Form.Control>
                                      </td>
                                    </tr>
                                ))}
                            </tbody>
                        </Table>

                      <Modal show={this.state.show} onHide={this.handleClose} animation={false}>
                        <Modal.Header closeButton>
                          <Modal.Title>新增帳號</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>
                          <Form onSubmit={this.handleSubmit}>
                            <Form.Group controlId="formGridUsername">
                              <Form.Label>Username</Form.Label>
                              <Form.Control type="text" name="new_username" required value={this.state.new_username} pattern="[a-zA-Z0-9]{8,16}" onChange={this.handleChange} />
                              <Form.Text className="text-muted">
                                Make sure it's at least 8 characters and at most 16 characters.
                              </Form.Text>
                            </Form.Group>
                            <Form.Group controlId="formGridName">
                              <Form.Label>Name</Form.Label>
                              <Form.Control type="text" name="new_name" required value={this.state.new_name} onChange={this.handleChange}/>
                            </Form.Group>
                            <Form.Group controlId="formGridEmail">
                              <Form.Label>Email</Form.Label>
                              <Form.Control type="email" name="new_email" required value={this.state.new_email} onChange={this.handleChange} />
                            </Form.Group>
                            <Form.Group controlId="formGridPassword">
                              <Form.Label>Password</Form.Label>
                              <Form.Control type="password" name="new_password" required value={this.state.new_password} onChange={this.handleChange} />
                              <Form.Text className="text-muted">
                                Make sure it's at least 8 characters and at most 16 characters.
                              </Form.Text>
                              <Form.Control as="select" name="new_role" value={this.state.new_role} onChange={this.handleSelectNewRole}>
                                <option>user</option>
                                <option>manager</option>
                              </Form.Control>
                            </Form.Group>
                            <Button variant="primary" type="submit">
                              Register
                            </Button>
                            <Form.Text className="text-muted">
                              By creating an account, you agree to the Terms of Service.
                            </Form.Text>
                          </Form>
                        </Modal.Body>
                      </Modal>
                  </Col>
              </Row>
          </Container>
      );
  }
}
