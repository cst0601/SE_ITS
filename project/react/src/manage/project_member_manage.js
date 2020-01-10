import React from 'react';
import { Form, Row, Col, Container, Table, ListGroup, Modal, Button, Badge } from 'react-bootstrap'
import { Global } from '../global.js'
import 'bootstrap/dist/css/bootstrap.css';

export default class ProjectMemberManage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      severity: "",
      show: false,
      username: "",
      project_name: "",
      members: [],
      new_member_name: "",
      new_member_manager: false,
      new_member_developer: false,
      new_member_tester: false,
      isManager: false
    };
    this.username = this.props.match.params.username;
    this.project_name = this.props.match.params.project_name;
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/project/member_list",
      {username: this.username,
       project_name: this.project_name}
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          this.setState(response.data.payload);
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
    this.addNewMember = this.addNewMember.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.removeMember = this.removeMember.bind(this);
    this.updateRole = this.updateRole.bind(this);
    this.changeNewRole = this.changeNewRole.bind(this);
  }

  handleClose() {this.setState({ show: false, new_member_name: "", new_member_role: "user" });}
  handleShow() {this.setState({ show: true });}

  handleChange(event) {
    const { name, value } = event.target;
    this.setState({ [name]: value });   /* <--- {} is for JSON :) */
  }

  directToProfile(username){
    this.props.history.push("/" + username);
  }

  removeMember(username) {
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/project/remove_member",
      {
        username: this.username,
        project_name: this.project_name,
        selected_username: username
      }
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          this.setState(response.data.payload);
          break;
        case "failure":
          alert(response.data.payload);
          break;
        default:
          alert("Web broken. Please refresh this page.");
      }
    });
  }

  updateRole(username, role, value) {
    if(!this.state.isManager)
      return;
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/project/update_member_role",
      {username: this.username,
       project_name: this.project_name,
       selected_username: username,
       role: role,
       value: !value
     }
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          this.setState(response.data.payload);
          break;
        case "failure":
          alert(response.data.payload);
          break;
        default:
          alert("Web broken. Please refresh this page.");
      }
    });
  }

  changeNewRole(role)
  {
    if(role == "manager"){
      this.setState({new_member_manager: !this.state.new_member_manager})
    }else if(role == "developer"){
      this.setState({new_member_developer: !this.state.new_member_developer})
    }else if(role == "tester"){
      this.setState({new_member_tester: !this.state.new_member_tester})
    }
  }

  addNewMember(event) {
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/project/add_new_member",
      {
        username: this.username,
        project_name: this.project_name,
        new_member_data: {
          username: this.state.new_member_name,
          manager: this.state.new_member_manager,
          developer: this.state.new_member_developer,
          tester: this.state.new_member_tester
        }
      }
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          this.setState(response.data.payload);
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

  render(){
      let projectLink = "/" + this.username + "/" + this.project_name;
      return(
          <Container>
              <Row style={{marginTop:"50px"}}>
                  <Col>
                      <p>
                        <a className="PageLink" href={"/" + this.username}>{this.username}</a>{" > "}
                        <a className="PageLink" href={projectLink}>{this.project_name}</a>{" > members"}
                      </p>
                      <h2>Project Member</h2>
                      {this.state.isManager ?
                        <div>
                          <Button id="button-add" variant="primary" onClick={this.handleShow}>
                            Add Member
                          </Button>
                        </div> : <div></div>
                      }
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
                                {this.state.members.map((member, index) => (
                                    <tr>
                                      <td onClick={() => this.directToProfile(member.username)}>{member.name}</td>
                                      <td>{member.email}</td>
                                      <td>
                                        {!member.owner ?
                                          <div>
                                            <Badge className="attribute" variant="dark" >
                                              <Badge className="level" variant={member.manager?"warning":"secondary"} onClick={() => this.updateRole(member.username, "manager", member.manager)}>manager</Badge>
                                              <Badge className="level" variant={member.developer?"warning":"secondary"} onClick={() => this.updateRole(member.username, "developer", member.developer)}>developer</Badge>
                                              <Badge className="level" variant={member.tester?"warning":"secondary"} onClick={() => this.updateRole(member.username, "tester", member.tester)}>tester</Badge>
                                            </Badge>
                                          </div> :
                                          <div>Owner</div>
                                        }
                                      </td>
                                      {console.log(member.owner)}
                                      {(this.state.isManager && !member.owner) &&
                                        <td>
                                          <Button id="button-remove" variant="danger" onClick={() => this.removeMember(member.username)}>
                                            Remove
                                          </Button>
                                        </td>
                                      }
                                    </tr>
                                ))}
                            </tbody>
                        </Table>

                      <Modal show={this.state.show} onHide={this.handleClose} animation={false}>
                        <Modal.Header closeButton>
                          <Modal.Title>新增成員</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>
                          <Form.Group controlId="formNewMemberName">
                            <Form.Label>請輸入成員名稱</Form.Label>
                            <Form.Control type="text" name="new_member_name" value={this.state.new_member_name} onChange={this.handleChange} />
                            <Badge className="attribute" variant="dark" >
                              <Badge className="level" variant={this.state.new_member_manager?"warning":"secondary"} onClick={() => this.changeNewRole("manager")}>manager</Badge>
                              <Badge className="level" variant={this.state.new_member_developer?"warning":"secondary"} onClick={() => this.changeNewRole("developer")}>developer</Badge>
                              <Badge className="level" variant={this.state.new_member_tester?"warning":"secondary"} onClick={() => this.changeNewRole("tester")}>tester</Badge>
                            </Badge>
                          </Form.Group>
                        </Modal.Body>
                        <Modal.Footer>
                          <Button variant="secondary" onClick={this.handleClose}>
                            Close
                          </Button>
                          <Button variant="primary" onClick={this.addNewMember}>
                            Add
                          </Button>
                        </Modal.Footer>
                      </Modal>
                  </Col>
              </Row>
          </Container>
      );
  }
}
