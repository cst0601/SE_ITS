import React from 'react';
import { Row, Col, Container, ListGroup, Badge } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.css';

class Issue extends React.Component {
    render() {
        return(
            <ListGroup.Item style={{padding: '5px'}}>
                <Row>
                    <Col><h5>{this.props.name}</h5></Col>
                    <Col align="right"><p>{this.props.response} responses</p></Col>
                </Row>
            </ListGroup.Item>
        );
    }
}

export default class IssueBoard extends React.Component {
    renderIssue(name, id, author, timestamp, response, lastUpdateTime) {
        return <Issue
                    name={name}
                    id={id}
                    author={author}
                    time={timestamp}
                    response={response}
                    lastUpdateTime={lastUpdateTime}
                />
    }

    renderOpenedIssue() {
        return (
            <ListGroup variant="flush">
                {this.renderIssue("NullPointerException", 5, "Firis Mustlud", "2020/05/20", 1, "2 days ago")}
                {this.renderIssue("Test failed", 32, "Yamamoto Isoroku", "1941/12/07", 10, "3 weeks ago")}
                {this.renderIssue("Got frontendphobia", 2147483647, "Sophie Neuenmuller", "2019/10/27", 16, "6 months ago")}
            </ListGroup>
        );
    }

    render() {
        return (
            <Container>
                <Row style={{paddingTop: '50px'}}>
                    <Col lg={12}>
                        <h2>Issue Statistical Board</h2>
                        <h3><Badge variant="warning">3 Issues σ ﾟ∀ ﾟ) ﾟ∀ﾟ)σ</Badge></h3>
                        {this.renderOpenedIssue()}
                    </Col>
                </Row>
            </Container>
        );
    }
}
