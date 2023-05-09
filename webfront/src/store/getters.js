const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  id: state => state.user.id,
  username: state => state.user.username,
  name: state => state.user.name,
  roles: state => state.user.roles,
  identifier: state => state.user.identifier,
  avatar: state => state.user.avatar,
  permission_routes: state => state.permission.routes,
  visitedViews: state => state.tagsView.visitedViews,
  cachedViews: state => state.tagsView.cachedViews,
  menuID: state => state.permission.menuID,
  menuBtn: state => state.permission.menuBtn,
  tempBtn: state => state.permission.tempBtn
}
export default getters
