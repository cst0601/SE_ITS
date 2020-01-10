import React from 'react';
import { Form, Button, Row, Col, Container, Modal } from 'react-bootstrap'
import { Global } from '../global.js'
import 'bootstrap/dist/css/bootstrap.css';
import './profile.css';
export default class Profile extends React.Component {  // export default is the class that is accessable from outside

  constructor(props) {
    super(props);
    this.profileLineNames = ["email", "username", "lineID", "name"];
    this.state = {
      email: "",
      username: "",
      lineID: "",
      oldPassword: "",
      newPassword: "",
      show: false,
      name: "",
      originProfileData: {
        email: "",
        username: "",
        lineID: "",
        name: ""
      },
      isOwner: false
    };
    this.username = this.props.match.params.username;
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/user/profile",
      {username: this.username}
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          this.setState(response.data.payload);
          this.setState({originProfileData: response.data.payload});
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
    this.isProfileChange = this.isProfileChange.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.onClickButtonProject = this.onClickButtonProject.bind(this);
    this.updateProfile = this.updateProfile.bind(this);
    this.updatePassword = this.updatePassword.bind(this);
  }
  handleChange(event) {
    const { name, value } = event.target;
    this.setState({ [name]: value });   /* <--- {} is for JSON :) */
  }

  onClickButtonProject = event =>{
    window.location = "/" + this.username + "/projects";
  }

  updateProfile(event) {
    const axios = require('axios');
    axios.post(
      "http://127.0.0.1:5000/user/update_profile",
      this.state
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          this.setState(response.data.payload);
          this.setState({originProfileData: response.data.payload});
          break;
        case "failure":
          alert(response.data.payload);
          break;
        default:
          alert("Web broken. Please refresh this page.");
      }
    });
  }

  updatePassword(event) {
    const axios = require('axios');
    axios.post(
      "http://127.0.0.1:5000/user/update_password",
      this.state
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          alert(response.data.payload);
          this.setState({ show: false, oldPassword: "", newPassword: "" });
          break;
        case "failure":
          alert(response.data.payload);
          break;
        default:
          alert("Web broken. Please refresh this page.");
      }
    });

  }

  handleClose() {this.setState({ show: false });}
  handleShow() {this.setState({ show: true });}
  isProfileChange() {
    for(var index in this.profileLineNames){
      if(this.state[this.profileLineNames[index]] !== this.state.originProfileData[this.profileLineNames[index]]){
        return true;
      }
    }
    return false;
  }
  render() {
    const { username, email, lineID, oldPassword, newPassword, name } = this.state;
    return (
      <Container>
        <Row style={{paddingTop: '50px'}}>
          <Col lg={12}>
            <h2>Profile</h2>
            <Form onSubmit={this.updateProfile}>
              <Form.Group controlId="formGridUsername">
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" name="username" readOnly value={username} ></Form.Control>
              </Form.Group>
              <Form.Group controlId="formGridName">
                <Form.Label>Name</Form.Label>
                <Form.Control type="text" name="name" required readOnly={this.state.isOwner? false : true} value={name} onChange={this.handleChange}/>
              </Form.Group>
              <Form.Group controlId="formGridEmail">
                <Form.Label>Email</Form.Label>
                <Form.Control type="email" required name="email" readOnly={this.state.isOwner? false : true} value={email} onChange={this.handleChange}/>
              </Form.Group>
              <Form.Group controlId="formGridEmail">
                <Form.Label>Line ID</Form.Label>
                <Form.Control type="text" name="lineID" readOnly={this.state.isOwner? false : true} value={lineID} onChange={this.handleChange}/>
              </Form.Group>
              <Form.Group controlId="formGridButton">
                {this.state.isOwner ?
                  <div>
                    <Button className="btn" variant="primary" type="submit" disabled={this.isProfileChange()? false : true}>
                      更新個人資料
                    </Button>
                    <br/>
                    <Button className="btn" variant="primary" onClick={this.handleShow}>
                      修改密碼
                    </Button>
                    <br/>
                    <Button className="btn" variant="primary" onClick={this.onClickButtonProject}>
                      我的專案
                    </Button>
                  </div> : <div></div>
                }
              </Form.Group>
            </Form>
            <Modal show={this.state.show} onHide={this.handleClose} animation={false}>
              <Modal.Header closeButton>
                <Modal.Title>修改密碼</Modal.Title>
              </Modal.Header>
              <Modal.Body>
              <Form.Group controlId="formOldPassword">
                <Form.Label>請輸入舊密碼</Form.Label>
                <Form.Control type="password" name="oldPassword" value={oldPassword} onChange={this.handleChange} />
              </Form.Group>
              <Form.Group controlId="formNewPassword">
                <Form.Label>請輸入新密碼</Form.Label>
                <Form.Control type="password" name="newPassword" value={newPassword} onChange={this.handleChange} />
              </Form.Group>
              </Modal.Body>
              <Modal.Footer>
                <Button variant="secondary" onClick={this.handleClose}>
                  Close
                </Button>
                <Button variant="primary" onClick={this.updatePassword}>
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
