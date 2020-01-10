import React from 'react';
import { Row, Col, Container, ListGroup, Tabs, Tab, Button} from 'react-bootstrap'
import { Global } from '../global.js'
import 'bootstrap/dist/css/bootstrap.css';
import './issue.css'
export default class IssueList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      show: false,
      username: "",
      project_name: "",
      issues: []
    };
    this.username = this.props.match.params.username;
    this.project_name = this.props.match.params.project_name;
    const axios = require('axios');
    axios.post(
      Global.backend_host + "/issue/list",
      {username: this.username,
       project_name: this.project_name}
    ).then(response => {
      switch(response.data.info) {
        case "redirect":
          window.location = window.location.origin + response.data.location;
          break;
        case "success":
          response.data.payload.sort((issueA, issueB) => {
            var dateA = new Date(issueA.last_update_time);
            var dateB = new Date(issueB.last_update_time);
            return dateB - dateA;
          });
          this.setState({ issues: response.data.payload});
          break;
        case "failure":
          alert(response.data.payload);
          break;
        default:
          alert("Web broken. Please refresh this page.");
      }
    });

    this.createIssue = this.createIssue.bind(this);
    this.linkToDashboard = this.linkToDashboard.bind(this);
    this.changePage = this.changePage.bind(this);
    this.listItem = this.listItem.bind(this);
  }
  getLoaclTime(timestamp){
    var date = new Date(timestamp);
    return date.toLocaleString();
  }
  createIssue(event) {
      this.props.history.push(
        "/" + this.username + "/" + this.project_name + "/issues/new");
  }
  linkToDashboard(event) {
      this.props.history.push(
        "/" + this.username + "/" + this.project_name + "/dashboard");
  }
  changePage(issue) {
    this.props.history.push(
      "/" + this.username + "/" + this.project_name + "/issues/" + issue.issue_number);

    /*window.location =
      "/issue?username=" + issue.username + "&project_name=" + issue.project_name + "&issue_id=" + issue.issue_id;*/
  }
  listItem(issueFilter) {
    return (<ListGroup>
      {this.state.issues.map(issue => {
        if (issueFilter(issue))
          return(
            <ListGroup.Item style={{padding: '5px'}} key={issue.issue_number} onClick={() => this.changePage(issue)} action>
                <Row>
                    <Col><h5>#{issue.issue_number} {issue.title}</h5></Col>
                    <Col align="right"><p>{issue.comment_amount} responses</p></Col>
                </Row>
                <Row>
                    <Col md={12}><p>Opened by {issue.creator} @ {this.getLoaclTime(issue.date)}</p></Col>
                    <Col md={12}><p>Last update on {this.getLoaclTime(issue.last_update_time)} </p></Col>
                </Row>
            </ListGroup.Item>
        );
      })}
    </ListGroup>);
  }


  render() {
    let projectLink = "/" + this.username + "/" + this.project_name;
      return (
          <Container>
              <Row style={{paddingTop: '50px'}}>
                  <Col lg={12}>
                      <p>
                        <a className="PageLink" href={"/" + this.username}>{this.username}</a>{" > "}
                        <a className="PageLink" href={projectLink}>{this.project_name}</a>{" > "}
                        issues{" "}
                      </p>
                      <h2>Issues</h2>
                      <Button id="button-add" variant="outline-primary" onClick={this.createIssue}>
                        New issue
                      </Button>
                      <Button id="button-board" variant="outline-primary" onClick={this.linkToDashboard}>
                        Issue Dashboard
                      </Button>
                      <Tabs defaultActiveKey="open" id="issue-tabs">
                          <Tab eventKey="open" title="Open">
                            {this.listItem((issue) => issue.state === "open")}
                          </Tab>
                          <Tab eventKey="closed" title="Closed">
                            {this.listItem((issue) => issue.state === "closed")}
                          </Tab>
                          <Tab eventKey="all" title="All">
                            {this.listItem((issue) => true)}
                          </Tab>
                      </Tabs>
                  </Col>
              </Row>
          </Container>
      );
  }
}
