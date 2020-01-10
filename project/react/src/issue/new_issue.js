import React from 'react';
import { Form, Button, Row, Col, Container } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.css';
import IssueProperties from './issue_properties.js';
import './new_issue.css';
import TextAreaWithFile from '../mark_down/text_area_with_file.js';
import { Global } from '../global.js'

export default class NewIssue extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      title: "",
      severity: "",
      priority: "",
      reproducible: "",
      assignee: "",
      assignees: [],
      comment: "",
      members: [],
      username: this.props.match.params.username,
      project_name: this.props.match.params.project_name
    };
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/project/member_list",
      {username: this.state.username,
       project_name: this.state.project_name}
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

    this.onAttributeChange = this.onAttributeChange.bind(this);
    this.handleCommentChange = this.handleCommentChange.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.onAssigneesChange = this.onAssigneesChange.bind(this);

  }
  handleChange(event) { // what the fuck is this function, I had enough with syntax sugar :(
    const { name, value } = event.target;
    this.setState({ [name]: value });
  }

  handleSubmit(event) {
    if (this.state.title == null && this.state.comment == null) {
      alert("Write something about this issue before submitting");
      return;
    }

    event.preventDefault();
    const axios = require('axios');
    axios.post(
      "http://127.0.0.1:5000/issue/new",
      this.state
    ).then(
      response => {
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
      }
    );

  }
  onDragOver(evt) {
    evt.preventDefault()

    if (this.props.disabled) return

    this.setState({ hightlight: true })
  }

  onDragLeave() {
    this.setState({ hightlight: false })
  }

  onDrop(event) {
    event.preventDefault()

    if (this.props.disabled) return

    const files = event.dataTransfer.files
    if (this.props.onFilesAdded) {
      const array = this.fileListToArray(files)
      this.props.onFilesAdded(array)
    }
    this.setState({ hightlight: false })
  }
  onAttributeChange(attributeName, value) {
    this.setState({ [attributeName]: value });
  }
  handleCommentChange(text) {
    this.setState({ comment: text });
  }
  onAssigneesChange(action, assignee) {
    let assignees = this.state.assignees;
    if(action === "add"){
      assignees.push(assignee);
    }else if(action === "delete"){
      assignees = assignees.filter(name => {
        return name != assignee;
      })
    }
    console.log({assignees: assignees});
    this.setState({assignees: assignees});
  }
  render() {
    let projectLink = "/" + this.state.username + "/" + this.state.project_name;
    return (
      <Container>
        <Form onSubmit={this.handleSubmit}>
          <Row style={{paddingTop: '50px'}}>
            <Col md={9}>
              <p>
                <a className="PageLink" href={"/" + this.state.username}>{this.state.username}</a>{" > "}
                <a className="PageLink" href={projectLink}>{this.state.project_name}</a>{" > "}
                <a className="PageLink" href={projectLink + "/issues"}>issues</a>{" > new"}
              </p>
              <h2>Create a new issue</h2>
              <Form.Group>
                <Form.Control required type="text" placeholder="Title" name="title" onChange={this.handleChange}/>
              </Form.Group>
              <Form.Group>
                  <Form.Label>Comment</Form.Label>
                  <TextAreaWithFile
                    onTextChange={this.handleCommentChange}
                    comment={this.state.comment}
                  />
              </Form.Group>
            </Col>
            <Col md={3}>
              <IssueProperties
                onAttributeChange={this.onAttributeChange}
                onAssigneesChange={this.onAssigneesChange}
                severity={this.state.severity}
                priority={this.state.priority}
                reproducible={this.state.reproducible}
                assignees={this.state.assignees}
                members={this.state.members}
              />
            </Col>
          </Row>
          <Button variant="primary" style={{width: '100%'}} type="submit">
            Submit new issue
          </Button>
        </Form>
      </Container>
    );
  }
}
