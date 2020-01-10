import React from 'react';
import { Form, Button, Row, Col, Container, ListGroup, Modal, Alert } from 'react-bootstrap'
import { Global } from '../global.js'
import 'bootstrap/dist/css/bootstrap.css';
import './project.css';
export default class ProjectList extends React.Component {  // export default is the class that is accessable from outside
  constructor(props) {
    super(props);
    this.state = {
      show: false,
      new_project_name: "",
      projects: [],
      showAlert: false
    };

    this.username = this.props.match.params.username;
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/project/list",
      {username: this.username}
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          this.setState({projects: response.data.payload});
          break;
        case "failure":
          alert(response.data.payload);
          break;
        default:
          alert("Web broken. Please refresh this page.");
      }
    });

    this.handleChange = this.handleChange.bind(this);
    this.handleProjectNameChange = this.handleProjectNameChange.bind(this);
    this.changePage = this.changePage.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.handleShow = this.handleShow.bind(this);
    this.createNewProject = this.createNewProject.bind(this);
  }

  handleChange(event) {
    const { name, value } = event.target;
    this.setState({ [name]: value });   /* <--- {} is for JSON :) */
  }
  handleProjectNameChange(event) {
    const { name, value } = event.target;
    console.log(value);
    var format = /[ ~!@#$%^&*()+\-=\[\]{};':"\\|,.<>\/?]/;
    this.setState({
      [name]: value,
      showAlert: format.test(value)
    });   /* <--- {} is for JSON :) */
  }
  changePage(project) {

    this.props.history.push("/" + project.username + "/" + project.project_name);
    // this.props.history.push("/project?username=" + project.username + "&project_name=" + project.project_name);
  }

  handleClose() {this.setState({ show: false });}
  handleShow() {this.setState({ show: true });}

  createNewProject(event) {
    event.preventDefault();
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/project/list/create_project",
      {project_name: this.state.new_project_name}
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          break;
        case "failure":
          alert(response.data.payload);
          break;
        default:
          alert("Web broken. Please refresh this page.");
      }
    });
  }

  render() {
    return (
      <Container>
        <Row style={{paddingTop: '50px'}}>
          <Col lg={12}>
            <p>
              <a className="PageLink" href={"/" + this.username}>{this.username}</a>{" > projects"}
            </p>
            <h2>My Project List</h2>
            <Button id="button-add" variant="outline-primary" onClick={this.handleShow}>
              新增專案
            </Button>

            <ListGroup>
              {this.state.projects.map(project => (
                <ListGroup.Item onClick={() => this.changePage(project)} action key={project.project_name}>
                  <h4> {project.project_name} </h4>
                  <p> create by {project.username}</p>
                </ListGroup.Item >
              ))}
            </ListGroup>

            <Modal show={this.state.show} onHide={this.handleClose} animation={false}>
              <Modal.Header closeButton>
                <Modal.Title>新增專案</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                <Form.Group controlId="formOldPassword">
                  <Form.Label>請輸入專案名稱</Form.Label>
                  <Form.Control type="text" name="new_project_name" value={this.state.new_project_name} onChange={this.handleProjectNameChange} />
                  <Alert variant="warning" show={this.state.showAlert}>
                    Name can't contain any special characters like " ", "~", "!", "-", "#", etc.
                  </Alert>
                </Form.Group>
              </Modal.Body>
              <Modal.Footer>
                <Button variant="secondary" onClick={this.handleClose}>
                  Close
                </Button>
                <Button variant="primary" disabled={this.state.showAlert} onClick={this.createNewProject}>
                  Save Changes
                </Button>
              </Modal.Footer>
            </Modal>

          </Col>
        </Row>
      </Container>
    );
  }
}
