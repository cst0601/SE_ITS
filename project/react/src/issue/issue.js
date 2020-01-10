import React from 'react';
import { Form, Button, Row, Col, Container, Badge, Card, Alert} from 'react-bootstrap'
import { Global } from '../global.js'
import 'bootstrap/dist/css/bootstrap.css';
import IssueProperties from './issue_properties.js';
import './issue.css';
import MarkDown from "../mark_down/mark_down.js"
import TextAreaWithFile from '../mark_down/text_area_with_file.js';
class Comment extends React.Component {
    render() {
        var date = new Date(this.props.timestamp);
        return (
            <Card>
                <Card.Header>{this.props.creator} commented on {date.toLocaleString()}</Card.Header>
                <Card.Body>
                  <MarkDown
                    source={this.props.text}
                  />
                </Card.Body>
            </Card>
        );
    }
}
class ChangeHistory extends React.Component {
    render() {
        var date = new Date(this.props.timestamp);
        return (
            <div style={{display: 'flex'}}>
              <div className="TimelineItem-badge ">
                  <svg className="octicon octicon-tag" viewBox="0 0 14 16" version="1.1" width="14" height="16" aria-hidden="true"><path fillRule="evenodd" d="M7.73 1.73C7.26 1.26 6.62 1 5.96 1H3.5C2.13 1 1 2.13 1 3.5v2.47c0 .66.27 1.3.73 1.77l6.06 6.06c.39.39 1.02.39 1.41 0l4.59-4.59a.996.996 0 000-1.41L7.73 1.73zM2.38 7.09c-.31-.3-.47-.7-.47-1.13V3.5c0-.88.72-1.59 1.59-1.59h2.47c.42 0 .83.16 1.13.47l6.14 6.13-4.73 4.73-6.13-6.15zM3.01 3h2v2H3V3h.01z"></path></svg>
              </div>
              {this.props.action === undefined ?
                <a style={{margin: '4px'}}>
                  <strong>{this.props.reporter}</strong>
                  {" set "}
                  <strong>{this.props.type}</strong>
                  {" to "}
                  <strong>{this.props.target}</strong>
                  {" on " + date.toLocaleString()}
                </a> :
                <a style={{margin: '4px'}}>
                  <strong>{this.props.reporter}</strong>{" " + this.props.action + " "}
                  <strong>{this.props.target}</strong>{this.props.action === "add" ? " into " : " from "}
                  <strong>{this.props.type}</strong>
                  {" on " + date.toLocaleString()}
                </a>}
            </div>
        );
    }
}
export default class Issue extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            comment_list: [],
            creator: "",
            date: 0,
            new_comment_description: "",
            issue_number: 0,
            title: "",
            severity: "",
            priority: "",
            reproducible: "",
            assignee: "",
            assignees: [],
            state: "",
            members: []
        }
        this.username = this.props.match.params.username;
        this.project_name = this.props.match.params.project_name;
        this.issue_number = this.props.match.params.issue_number;
        const axios = require('axios');
        axios.post(
          Global.backend_host + "/issue/get_issue_content",
          {username: this.username,
           project_name: this.project_name,
           issue_number: this.issue_number}
        ).then(response => {
          switch(response.data.info) {
            case "redirect":
              window.location = window.location.origin + response.data.location;
              break;
            case "success":
              response.data.payload.comment_list.sort((commentA, commentB) => {
                var date1 = new Date(commentA.date);
                var date2 = new Date(commentB.date);
                return date1 - date2;
              })
              this.setState(response.data.payload);
              break;
            case "failure":
              alert(response.data.payload);
              break;
            default:
              alert("Web broken. Please refresh this page.");
          }
        });
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

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.onAttributeChange = this.onAttributeChange.bind(this);
        this.handleCommentChange = this.handleCommentChange.bind(this);
        this.handleChangeIssueState = this.handleChangeIssueState.bind(this);
        this.onAssigneesChange = this.onAssigneesChange.bind(this);

    }
    handleSubmit(event) {
      event.preventDefault();
      const axios = require('axios');
      axios.post(
        "http://127.0.0.1:5000/issue/new_comment",
        {username: this.username,
         project_name: this.project_name,
         issue_number: this.issue_number,
         comment: this.state.new_comment_description}
      ).then(response => {
        switch(response.data.info) {
          case "redirect":
            window.location = window.location.origin + response.data.location;
            break;
          case "success":
            response.data.payload.comment_list.sort((commentA, commentB) => {
              var date1 = new Date(commentA.date);
              var date2 = new Date(commentB.date);
              return date1 - date2;
            })
            response.data.payload.new_comment_description = ""
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
    handleChange(event) {
      const { name, value } = event.target;
      this.setState({ [name]: value });
    }
    onAttributeChange(attributeName, value) {
      let changeDetail = { [attributeName]: value };
      this.setState(changeDetail);
      const axios = require('axios');
      axios.post(
        "http://127.0.0.1:5000/issue/change_attribute",
        {username: this.username,
         project_name: this.project_name,
         issue_number: this.issue_number,
         change_detail: changeDetail}
      ).then(response => {
        switch(response.data.info) {
          case "redirect":
            window.location = window.location.origin + response.data.location;
            break;
          case "success":
            response.data.payload.comment_list.sort((commentA, commentB) => {
              var date1 = new Date(commentA.date);
              var date2 = new Date(commentB.date);
              return date1 - date2;
            })
            response.data.payload.new_comment_description = ""
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
    onAssigneesChange(action, assignee) {
      let assignees = this.state.assignees;
      if(action === "add"){
        assignees.push(assignee);
      }else if(action === "delete"){
        assignees = assignees.filter(name => {
          return name != assignee;
        })
      }
      this.setState({assignees: assignees});
      const axios = require('axios');
      axios.post(
        "http://127.0.0.1:5000/issue/change_assignee",
        {username: this.username,
         project_name: this.project_name,
         issue_number: this.issue_number,
         change_detail: {
           assignees: assignees,
           action: action,
           target: assignee
         }
        }
      ).then(response => {
        switch(response.data.info) {
          case "redirect":
            window.location = window.location.origin + response.data.location;
            break;
          case "success":
            response.data.payload.comment_list.sort((commentA, commentB) => {
              var date1 = new Date(commentA.date);
              var date2 = new Date(commentB.date);
              return date1 - date2;
            })
            response.data.payload.new_comment_description = ""
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
    handleCommentChange(text) {
      this.setState({ new_comment_description: text });
    }
    handleChangeIssueState(event) {
      let targetState = this.state.state === "open" ? "closed" : "open"
      this.onAttributeChange("state", targetState);
    }
    render() {
        let projectLink = "/" + this.username + "/" + this.project_name;
        return (
            <Container style={{paddingTop: '50px', paddingBottom: '50px'}}>
                <Row>
                    <Col>
                        <p>
                          <a className="PageLink" href={"/" + this.username}>{this.username}</a>{" > "}
                          <a className="PageLink" href={projectLink}>{this.project_name}</a>{" > "}
                          <a className="PageLink" href={projectLink + "/issues"}>issues</a>{" "} > {this.issue_number}
                        </p>
                        <h2>{this.state.title} #{this.issue_number}</h2>
                        <h4><Badge variant={this.state.state === "open" ? "success" : "warning"}>{this.state.state}</Badge></h4>
                    </Col>
                </Row>
                <Row style={{paddingTop: '10px'}}>
                    <Col className="MainList" lg={8}>

                        <Comment creator={this.state.creator} timestamp={this.state.date} text={this.state.comment} key={this.state.creator + this.state.date} />
                        {this.state.comment_list.map(comment => (
                          comment.type === undefined ?
                            <Comment creator={comment.creator} timestamp={comment.date} text={comment.comment} key={comment.date}/> :
                            <ChangeHistory reporter={comment.creator} timestamp={comment.date} type={comment.type} target={comment.target} action={comment.action} key={comment.date}/>
                        ))}
                        <Card>
                            <Card.Body>
                              <Form onSubmit={this.handleSubmit}>
                                <Form.Group>
                                  <TextAreaWithFile
                                    onTextChange={this.handleCommentChange}
                                    comment={this.state.new_comment_description}
                                  />
                                <Button style={{marginTop: "5px"}} variant="outline-primary" type="submit" disabled={this.state.new_comment_description === ""}>Submit Comment</Button>
                                <Button style={{marginTop: "5px"}} variant="outline-warning" onClick={this.handleChangeIssueState}>{this.state.state === "open" ? "Close" : "Reopen"} Issue</Button>
                                </Form.Group>
                              </Form>
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col lg={4}>
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
            </Container>
        );
    }
}
