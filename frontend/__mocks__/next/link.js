const mockLink = ({ children, href }) => <children.type {...children.props} href={href} />

export default mockLink
