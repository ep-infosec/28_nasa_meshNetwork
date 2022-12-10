Network Design
==============
The mesh network functions by assigning time blocks to individual network nodes.  A node is any entity communicating using the mesh network protocol.  The time allocations are determined using a time division multiple access-based architecture.  This architecture is illustrated in the figure below.  Time is sliced in segments called Frames.  A **Frame** consists of the **Cycle**, **Admin**, and the **Sleep** periods.  Primary communication across the network is performed during the Cycle.  The Cycle is broken down into Slots, where a **Slot** is the portion of time provided to each node to perform its outgoing communication on the network.  All time lengths within the Frame are configurable parameters allowing the network configuration to be tuned for a particular application.

During a Slot, only one node is transmitting, and all other nodes are listening.  To ensure data integrity and accommodate some variation of clock times across the network, delay periods are built into the communication protocol.  As shown in the figure, this pattern of delays is designed to ensure that receiving nodes are listening for the entirety of the transmitting node’s transmission.  Once a node is done transmitting, it will change over into receive mode and prepare to listen to other transmitting nodes.  The lengths of the sub-periods within the slot are configurable, so as to make the network architecture flexible for specific applications.

Once all slots are completed, the Cycle ends, and the Admin period begins.  The Admin period is used by the network to exchange network administration data.  The administration data consists of messages that are produced and consumed solely by the network nodes and not passed to each node's host platform.  The Admin period can also be used to perform a Block Transmit.  A Block Transmit allows one node to transfer a large set of data across the network.  The Block Transmit is designed to be used for a data set that can not fit in a single slot or handful of slot periods.  A host can request a block ttransmit from its node, and if the network accepts the request, the provided data block will be passed over the network.  

Finally, after the Admin period, a Sleep period begins for the remaining time in the Frame.  During the Sleep, all nodes are nominally quiescent, allowing for power-savings when communication is not necessary.

Because all the lengths of the elements of the TDMA Frame are configurable parameters, the network can be tailored to fit a particular customer's use case.  For example, for low latency, the Frame length could be set to 1 second, so that each node will be able communicate data at a 1 Hz rate.  Conversely, if low latency is not a requirement, the Frame length could be extended to provide larger bandwidth for each node but a lower rate.  The allotment of time between the Cycle and Admin periods can also be traded.  More time could be allocated to Admin for example by shortening the Slots, allowing for more bandwidth for block transfers. 

.. figure:: ../tdma_frame.png
   :align: center

   Mesh Network TDMA Frame

To function without a master node, the nodes in the network require a common time source to maintain the integrity of the TDMA architecture.  The system is not dependent on a specific method of synchronizing time, but the reference design was developed and tested assuming the individual node clocks are synced using time received from the Global Positioning System (GPS).  Since GPS is widely used already by spacecraft for orbital position and other data, it is a convenient, readily available, and reliable time source.

Network Topology and Data Relay
-------------------------------

The network topology employed is a simple point-to-point design, as illustrated in the figure below.  When nodes broadcast, all other nodes in range receive the data.  Any nodes not in range of a broadcasting node will not receive its data directly during the initial transmission.

.. figure:: ../topology.png
   :align: center

   Mesh Network Topology

However, using the data relay capability in the network, nodes will transmit not only their own data, but also data received from other nodes.  The relay functionality is performed in a single repeat manner, meaning that nodes will only rebroadcast unique data once.  For example, for the network shown in the figure above, Node 2 would receive data from Nodes 1 and 4 directly.  When Node 2 enters its transmission period, it would pass its own data and any data received from Node 1 back out to be received by Nodes 1 and 4.  When Node 1 receives this transmission from Node 2, it will recognize the portion of the message that it originally transmitted.  The next time that Node 1 transmits, it will not retransmit that portion of the data again.  This prevents data that was previously sent from being relayed back and forth across the network endlessly.

Each node within the network maintains a network graph of all the links between nodes across the network.  Before relaying data, this graph is referenced to determine whether the current node is on the shortest path between the original source and the destination node.  If the current node is not on the shortest path, the current node will not relay the data in order to reduce unnecessary network traffic.  The network graph is updated at a regular frequency to ensure that any network topology changes are captured, so that relay decisions are made appropriately.  

Because there is no master node, the network will continue to function regardless of what specific nodes are currently present in the network.  Any node present will transmit during its allotted Slot and receive data from other nodes during their Slots.  If a previously present node drops out of the network, the other nodes will notice the data dropout during the lost node’s Slot, but the network will remain intact for usage by the remaining nodes.  Since the network topology is point-to-point, any node that couldn’t communicate directly with other network nodes without going through the lost node will become isolated.  For example, if Node 1 dropped out of the network, Nodes 3 and 6 would also lose communication with the network.

Network Administration
----------------------

Without a network master, decisions to be made by the network require unanimous approval before implementation.  Network decisions are executed using a polling mechanism implemented by the mesh network.  For commands requiring approval prior to implementation, each node will create a poll and compile poll responses received from the rest of the network.  Decision on the poll is not made until responses are received from all active nodes.  

If a node is determined to be in error in some way, another node may command a change to fix the node in error, such as a configuration update or node restart for the node in error.  In this case, the vote of the potentially errant node is excluded from the polling.  The remaining nodes must then reach a unanimous decision on whether to implement the fix on the errant node.  Polling also acts as a guard against a single errant node attempting to fix other nodes that are already functioning correctly.  The correctly functioning nodes would detect the command from the errant node and reject the requested change.
