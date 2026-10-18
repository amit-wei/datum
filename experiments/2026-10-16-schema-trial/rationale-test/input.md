### R1
Statement: The system shall acquire data from a defined source on the schedule that its definition states, without an action by the user.
Links:
- of: function Acquisition: Obtains data from a defined source. The platform asks the source on the schedule that the definition states, or the source sends the data without a request.
- parent: requirement: The platform shall acquire life data from defined external sources without an action by the user.

### R2
Statement: The system shall not serve to a caller a part of life state that the position of that caller does not admit.
Links:
- of: function Admission by Position: Refuses a read, a write and a removal that the position of the caller does not admit.
- parent: requirement: The platform shall serve to an agent only the part of what it holds that the position of the agent admits. The platform shall accept from an agent a write only to the part of what it holds that its position admits.

### R3
Statement: The system shall report a change to the definition of an external source that widens the data that the platform acquires.
Links:
- of: function Source Definition: Holds the definition of each external source: what it is, what data it delivers, and how often it delivers it. Keeps that definition through its life, from the first statement to its removal.
- parent: requirement: The platform shall tell the difference between an action that needs the authorization of the user and an action that does not. The platform shall not do an action that needs authorization until it records an affirmative answer to a request that states that action.

### R4
Statement: The system shall restore the declared classes and the parties that count as the user from a copy that it gave.
Links:
- of: function Copy and Restoration: Gives a copy of the declared classes and of the parties that count as the user that is of a state that the system held at one time, and restores them from such a copy.
- parent: requirement: The loss of the host shall not cause the loss of life state, of what states an agent, or of the declared kinds of item, subjects, classes of action, parties that count as the user, acts and sources.

### R5
Statement: The system shall refuse a write that states its writer.
Links:
- of: function Write Admission: Accepts a write of an item from a writer inside the platform, and refuses a write that does not meet the contract.
- parent: requirement: The platform shall state the writer of a record that it holds and the time of that record. The platform shall not accept the writer or the time from the caller that supplied the record.

### R6
Statement: The system shall not give an agent the state that it holds to identify the user and to carry an exchange.
Links:
- of: function User Identification: Identifies the user.
- parent: requirement: The platform shall serve to an agent only the part of what it holds that the position of the agent admits. The platform shall accept from an agent a write only to the part of what it holds that its position admits.

### R7
Statement: The system shall deliver a message by the means that its unit of work states.
Links:
- of: function Message Delivery: Delivers a message to the user.
- parent: requirement: The platform shall deliver messages to the user that the user did not request. For each message, the platform shall record the condition that started it and the values that satisfied the condition.

### R8
Statement: The system shall accept a change to a declared class.
Links:
- of: function Class Declaration: Holds each declared class of action, with whether it needs the authorization of the user and with the writer that declared it. Accepts the declaration of a class, a change to a class and the removal of a class. Gives the declared classes to a caller.
- parent: requirement: The platform shall accept, for each kind of declaration that it holds, a new declaration, a change to a declaration, and the removal of a declaration.

### R9
Statement: The system shall refuse a write of an item of the kind of an exchange from a writer other than Interaction.
Links:
- of: function Write Admission: Accepts a write of an item from a writer inside the platform, and refuses a write that does not meet the contract.
- parent: requirement: The platform shall hold life state as one body. Each item shall show its origin. The platform shall not give a superseded value as the current value of an observed item.

### R10
Statement: The system shall receive from the host each delivery that the host routes to the platform.
Links:
- of: function Inbound Delivery: Accepts a delivery that an external service sends without a request, and gives it to Ingestion.
- parent: requirement: The platform shall acquire life data from defined external sources without an action by the user.

### R11
Statement: The system shall accept from Agent Definition the cost of the use of each model.
Links:
- of: function Call Record: Gives Self-Observation, for each call that it carries, the service, the system that called, the agent that the caller states, the time, the outcome, the usage and the cost.
- parent: requirement: The recurring cost of operation shall not be more than USD 50 each month. This cost does not include the host.

### R12
Statement: The system shall give whether any declared act names a given connection.
Links:
- of: function Act Declaration: Holds each declared act on the outside world, with the connection that it reaches, the form of its arguments and the writer that declared it. Accepts the declaration of an act, a change to an act and the removal of an act.
- parent: requirement: The platform shall accept, for each kind of declaration that it holds, a new declaration, a change to a declaration, and the removal of a declaration.

### R13
Statement: The system shall end the identification of the user after TBD with no exchange.
Links:
- answers: risk: The system accepts an exchange from a person who is not the user. Effect: Life state is disclosed. Work is raised in the name of the user.
- parent: requirement: The platform shall record the answer of the user as the platform received it from the user. The platform shall not accept an answer of the user that an agent states.

### R14
Statement: The system shall give Interaction at most one notice of stopped units of work in each period of TBD, which states each stop that it was given since its last such notice.
Links:
- answers: risk: The system floods the user with notices of stopped units. Effect: The user gets many notices for one fault, and stops reading them.
- parent: requirement: When the platform cannot continue to operate without an action, the platform shall raise work for that action. Where that action needs the user, the platform shall put a question to the user or send the user a message.

### R15
Statement: The system shall give Self-Observation the number of units of work that it holds and that are not closed.
Links:
- answers: risk: The system holds more work that is not closed than the platform can run. Effect: Every answer is late. Nothing has failed, so nothing reports a fault.
- parent: requirement: The platform shall continue work when no client is connected. For any work that it holds, the platform shall give the agent that is responsible, the system or the agent that raised it, the current state, and the work that caused it.

### R16
Statement: The system shall show, with the state of the platform, the time at which Self-Observation gave it.
Links:
- answers: risk: The view of the platform shows a state of the platform that is not current as current. Effect: The user reads that the platform is well while it is not.
- parent: requirement: The platform shall report its cost of operation for the current period. The platform shall report its own operational state and the operational state of its external sources.

### R17
Statement: The system shall give a position within TBD.
Links:
- of: function Position Declaration: Holds each position with the part of each body and the acts that it admits, with the positions that its holder may confer, and with the positions whose holders it may retire. Accepts the declaration of a position, a change to a position and the removal of a position. Gives a position to a boundary that refuses.
- parent: requirement: The platform shall direct work to agents in a declared hierarchy. The platform shall let an agent get an answer from another agent. An agent shall act only inside the authority that its position gives. An answer from another agent shall not increase that authority.

### R18
Statement: The system shall report, at an interval of TBD, when life state cannot be restored from the copy away from the host.
Links:
- of: function Off-host Copy: Makes the copy of life state and of the declared kinds and subjects away from the host, decides when to make it, and restores them from it.
- parent: requirement: The loss of the host shall not cause the loss of life state, of what states an agent, or of the declared kinds of item, subjects, classes of action, parties that count as the user, acts and sources.

### R19
Statement: The platform shall complete the work that it accepts, or state a reason that is true where the work cannot end without the user or an external service, for at least TBD of that work.
Links:
- of: function Work Management: Holds work as tasks. Keeps the tasks through sessions and interruptions.

### R20
Statement: The platform shall use, in each answer that depends on it, what it has been told and what it holds, including what has changed since, in at least TBD of cases.
Links:
- of: function Life State Custody: Holds the data that describes the life of the user. Organises it and serves it. All agents read the same data.
