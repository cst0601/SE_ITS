import React from 'react';
import { Dropdown, ListGroup, Badge, Alert, Button} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.css';
import './issue_properties.css';
/**
 * Notes left by Chikuma : I'll find a better way to fix this indent problem
 * I know it looks wired now :(
*/
class CloseButton extends React.Component {
  render() {
    return (
      <Button className="close" onClick={this.props.onClick} variant="light" style={{backgroundColor: "white", position: "absolute", right: "0px"}}>
        <span >×</span>
      </Button>
    );
  }
}
export default class IssueProperties extends React.Component {
  constructor(props) {
    super(props);

    this.changeLevel = this.changeLevel.bind(this);
    this.addAssignee = this.addAssignee.bind(this);
    this.deleteAssignee = this.deleteAssignee.bind(this);
  }
  changeLevel(parent, level) {
    if(this.props[parent] !== level)
      this.props.onAttributeChange(parent, level);
  }
  addAssignee(e, assignee) {
    this.props.onAssigneesChange("add", assignee);
  }
  deleteAssignee(assignee) {
    this.props.onAssigneesChange("delete", assignee);
  }
  render() {
    return (
      <ListGroup variant="flush">
        <ListGroup.Item>
          Assignees
          <ListGroup>
            {this.props.assignees.map((assignee) =>
              <ListGroup.Item className="NameList" key={assignee}>
                {assignee}
                <CloseButton onClick={() => this.deleteAssignee(assignee)}/>
              </ListGroup.Item>)
            }
          </ListGroup>
          <Dropdown>
            <Dropdown.Toggle variant="outline-dark" id="dropdown-basic" style={{marginTop: "5px"}}>
              Add Assignee
            </Dropdown.Toggle>
            <Dropdown.Menu>
                {this.props.members.map((member) => this.props.assignees.includes(member.username) ? console.log(member.username) : <Dropdown.Item key={member.username} onClick={e => this.addAssignee(e, member.username)}>{member.username}</Dropdown.Item>)}
            </Dropdown.Menu>
          </Dropdown>
        </ListGroup.Item>
        <ListGroup.Item>
          Attribute
          <div>
            <Badge className="attribute" variant="dark">
              severity:
              <Badge className="level" variant={this.props.severity==="low"?"success":"secondary"} onClick={(e) => this.changeLevel("severity", "low")}>low</Badge>
              <Badge className="level" variant={this.props.severity==="medium"?"warning":"secondary"} onClick={(e) => this.changeLevel("severity", "medium")}>medium</Badge>
              <Badge className="level" variant={this.props.severity==="high"?"danger":"secondary"} onClick={(e) => this.changeLevel("severity", "high")}>high</Badge>
            </Badge>
            <Badge className="attribute" variant="dark">
              priority:
              <Badge className="level" variant={this.props.priority==="low"?"success":"secondary"} onClick={(e) => this.changeLevel("priority", "low")}>low</Badge>
              <Badge className="level" variant={this.props.priority==="medium"?"warning":"secondary"} onClick={(e) => this.changeLevel("priority", "medium")}>medium</Badge>
              <Badge className="level" variant={this.props.priority==="high"?"danger":"secondary"} onClick={(e) => this.changeLevel("priority", "high")}>high</Badge>
            </Badge>
            <Badge className="attribute" variant="dark">
              reproducible:
              <Badge className="level" variant={this.props.reproducible==="yes"?"success":"secondary"} onClick={(e) => this.changeLevel("reproducible", "yes")}>yes</Badge>
              <Badge className="level" variant={this.props.reproducible==="no"?"danger":"secondary"} onClick={(e) => this.changeLevel("reproducible", "no")}>no</Badge>
            </Badge>
          </div>
        </ListGroup.Item>
      </ListGroup>
    );
  }
}
