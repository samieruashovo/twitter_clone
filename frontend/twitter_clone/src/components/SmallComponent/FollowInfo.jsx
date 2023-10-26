export const FollowInfo = ({ number = 0, followinfo = "" }) => {
  return (
    <div className="d-flex">
      <span className="bold-text">{number + "  " + followinfo}</span>
      {/* <span className="mx-2 side-name">{followinfo}</span> */}
    </div>
  );
};
