function Header({ siteName, enrolledCount }) {
  return (
    <header className="site-header">
      <div className="site-name">{siteName}</div>
      <nav>
        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#courses">Courses</a></li>
          <li><a href="#profile">Profile</a></li>
        </ul>
      </nav>
      <div className="enrolled-count">Enrolled: {enrolledCount}</div>
    </header>
  );
}

export default Header;