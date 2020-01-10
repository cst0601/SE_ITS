import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import SignIn from './sign_in/sign_in.js';
import SignUp from './sign_up/sign_up.js';
import Profile from './profile/profile.js';
import ProjectList from './project/projectlist.js';
import Project from './project/project.js';
import Issue from './issue/issue.js';
import NewIssue from './issue/new_issue.js';
import IssueList from './issue/issue_list.js';
import IssueBoard from './issue/issue_board.js';
import NavigatorBar from './navigator_bar.js';
import AccountManage from './manage/accountmanage.js';
import ProjectMemberManage from './manage/project_member_manage.js';
import Dashboard from './dashboard/dashboard.js'
import NotFound from './not_found.js'
import { BrowserRouter, Route } from 'react-router-dom';
import { Switch } from 'react-router';
// Redirect => document
class Its extends React.Component {
  render() {
        //<Redirect exact from="/" to="/login" />
    return (
      <BrowserRouter>
        <NavigatorBar/>
        <Switch>
          <Route path="/404" component={NotFound} />
          <Route path="/sign_in" component={SignIn} />
          <Route path="/sign_up" component={SignUp} />
          <Route path="/accountmanage" component={AccountManage} />
          <Route path="/:username/:project_name/issues/new" component={NewIssue} />
          <Route path="/:username/:project_name/issues/:issue_number" component={Issue} />
          <Route path="/:username/:project_name/dashboard" component={Dashboard} />
          <Route path="/:username/:project_name/issues" component={IssueList} />
          <Route path="/:username/:project_name/members" component={ProjectMemberManage} />
          <Route path="/:username/projects" component={ProjectList} />
          <Route path="/:username/:project_name" component={Project} />
          <Route path="/:username" component={Profile} />
        </Switch>
      </BrowserRouter>
    );
  }
}

// ========================================

/* Load from here :) */
ReactDOM.render(<Its />, document.getElementById("root"));
