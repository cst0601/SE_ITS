import React from 'react';
import { Form, Button, Row, Col, Container, Card} from 'react-bootstrap'
import { Global } from '../global.js'
import 'bootstrap/dist/css/bootstrap.css';
import './project.css';
import Dropzone from './dropzone'
import MarkDown from "../mark_down/mark_down.js"
import TextAreaWithFile from '../mark_down/text_area_with_file.js';

export default class Project extends React.Component {  // export default is the class that is accessable from outside
  constructor(props) {
    super(props);
//?=

    this.state = {
      username: "",
      project_name: "",
      description: "",
      inputEnable: false,
      owner: false
    };
    this.username = this.props.match.params.username;
    this.project_name = this.props.match.params.project_name;
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/project/get_project",
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

    this.handleChange = this.handleChange.bind(this);
    this.changeState = this.changeState.bind(this);
    this.updateDescription = this.updateDescription.bind(this);
    this.changeToIssueList = this.changeToIssueList.bind(this);
    this.changeToMemberList = this.changeToMemberList.bind(this);
    this.onFilesAdded = this.onFilesAdded.bind(this);
    this.handleDescriptionChange = this.handleDescriptionChange.bind(this);
    this.deleteProject = this.deleteProject.bind(this);
  }

  handleChange(event) {
    const { name, value } = event.target;
    this.setState({ [name]: value });   /* <--- {} is for JSON :) */
  }
  changeState(event) {
    if(this.state.inputEnable){
      this.updateDescription();
    }
    this.setState({inputEnable: !this.state.inputEnable});
  }
  updateDescription(event) {
    /* Send the inputed information to backend via POST */
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/project/update_description",
      {username: this.username,
       project_name: this.project_name,
       description: this.state.description}
    ).then(function (response) {
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
  changeToIssueList() {

    this.props.history.push("/" + this.username + "/" + this.project_name + "/issues");
    // this.props.history.push("/project?username=" + project.username + "&project_name=" + project.project_name);
  }
  changeToMemberList() {
    this.props.history.push("/" + this.username + "/" + this.project_name + "/members");
  }
  onFilesAdded(files) {
    this.setState(prevState => ({
      files: prevState.files.concat(files)
    }));
  }
  handleDescriptionChange(text) {
    this.setState({description: text});
  }
  deleteProject(){
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/project/delete_project",
      {username: this.username,
       project_name: this.project_name}
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          alert("Project deleted successfully.");
          this.props.history.push("/" + this.username + "/projects");
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
              <a className="PageLink" href={"/" + this.username}>{this.username}</a>{" > "}{this.project_name}
            </p>
            <Card>
              <Card.Header>
                <Card.Text as="label" className="label-title">{this.state.project_name}</Card.Text>
                <Button variant="outline-dark" className="button-right" onClick={this.changeToIssueList}>
                  Issues
                </Button>
                <Button variant="outline-primary" className="button-right" onClick={this.changeToMemberList}>
                  Members
                </Button>
              </Card.Header>
              <Card.Body>
                <Form.Group >
                  {this.state.inputEnable ?
                    <TextAreaWithFile
                      onTextChange={this.handleDescriptionChange}
                      comment={this.state.description}
                    /> :
                    <div style={{minHeight: "200px",border: "1px solid #ced4da", borderRadius: "0.25rem", padding: "0.375rem 0.75rem"}}>
                      <MarkDown
                        source={this.state.description}
                      />
                    </div>}
                  <Button variant="outline-success" className="button-right" style={{marginTop: '20px'}} onClick={this.changeState}>
                    {this.state.inputEnable ? "Save" : "Edit"}
                  </Button>
                </Form.Group>
              </Card.Body>
            </Card>
            {this.state.owner ?
              <div>
                <Button variant="danger" className="button-right" onClick={this.deleteProject}>
                  刪除專案
                </Button>
              </div> : <div></div>
            }
          </Col>
        </Row>
      </Container>
    );
    /*<Button variant="danger" className="button-right">
      Remove
    </Button>
    <Button variant="primary" className="button-right">
      Upload
    </Button>*/
  }
}
