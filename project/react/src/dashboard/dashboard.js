import React from 'react';
import { Row, Col, Container, ListGroup, Tabs, Tab, Button, Dropdown, Card, Badge, Form} from 'react-bootstrap'
import { Global } from '../global.js'
import './dashboard.css';
class MemberSelect extends React.Component {

  onSelectedChange = (username) => {
    this.props.onSelectedChange(username);
  }
  render() {
    return(
      <div>
        <h4>Select Member</h4>
        <Dropdown>
          <Dropdown.Toggle variant="outline-dark" id="dropdown-basic" style={{marginTop: "5px"}}>
            {this.props.selected === "" ? "all" : this.props.selected}
          </Dropdown.Toggle>
          <Dropdown.Menu>
            <Dropdown.Item onClick={e => this.onSelectedChange("")}>all</Dropdown.Item>
            {this.props.members.map((member) => <Dropdown.Item onClick={e => this.onSelectedChange(member.username)} key={member.username}>{member.username}</Dropdown.Item>)}
          </Dropdown.Menu>
        </Dropdown>
      </div>
    );
  }
}

class BoardCard extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Card>
                <Card.Body>
                    <Card.Title>
                        {this.props.title}
                        <Badge variant="success">{this.props.issues.length}</Badge>
                    </Card.Title>
                    <div className="pt-1">
                        <Card.Subtitle className="mb-2 text-muted">{this.props.description}</Card.Subtitle>
                        <ListGroup variant="flush">
                          {this.props.issues.map(issue =>
                            <ListGroup.Item key={issue.title}><a className="PageLink" href={this.props.link + "/issues/" + issue.issue_number}>{issue.title}</a></ListGroup.Item>
                          )}
                        </ListGroup>
                    </div>
                </Card.Body>
            </Card>
        );
    }
}

export default class Dashboard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          show: false,
          username: "",
          project_name: "",
          issues: [],
          members: [],
          selected_username: ""
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
                console.log(dateB - dateA);
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

        this.onSelectedChange = this.onSelectedChange.bind(this);
    }
    onSelectedChange(username){
      this.setState({selected_username: username});
    }
    getIssues = (state) => {
      let issues = this.state.issues.filter(issue => {
        if(this.state.selected_username !== ""){
          if(issue.assignees.includes(this.state.selected_username)){
            return true
          }
        }else{
          return true
        }
        return false
      })
      return issues.filter(issue => issue.state === state);
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
                      <a className="PageLink" href={projectLink + "/issues"}>issues</a>{" > Dashboard"}
                    </p>
                    <h1>Dashboard</h1>
                  </Col>
                </Row>
                <Row style={{paddingTop: '5px'}}>
                    <MemberSelect
                      selected={this.state.selected_username}
                      onSelectedChange={this.onSelectedChange}
                      members={this.state.members}
                    />
                </Row>
                <Row style={{paddingTop: '5px'}}>
                    <Col md={6} lg={6}>
                        <BoardCard
                          title="Open"
                          description={this.state.selected_username === "" ? "List of the opened issues of this project" : "List of the opened issues assigned to " + this.state.selected_username}
                          issues={this.getIssues("open")}
                          link={"/" + this.username + "/" + this.project_name}
                        />
                    </Col>
                    <Col md={6} lg={6}>
                        <BoardCard
                          title="Closed"
                          issues={this.getIssues("closed")}
                          description={this.state.selected_username === "" ? "List of the closed issues of this project" : "List of the closed issues assigned to " + this.state.selected_username}
                        />
                    </Col>
                </Row>
            </Container>
        );
    }
}
