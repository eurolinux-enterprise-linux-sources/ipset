# Range: Try to create from an invalid range
1 ipset -N test macipmap --from 2.0.0.1 --to 2.1.0.1
# Range: Create a set from a valid range
0 ipset -N test macipmap --from 2.0.0.1 --to 2.1.0.0
# Range: Add lower boundary
0 ipset -A test 2.0.0.1
# Range: Add upper boundary
0 ipset -A test 2.1.0.0
# Range: Test lower boundary
0 ipset -T test 2.0.0.1
# Range: Test upper boundary
0 ipset -T test 2.1.0.0
# Range: Test value not added to the set
1 ipset -T test 2.0.0.2
# Range: Test value before lower boundary
1 ipset -T test 2.0.0.0
# Range: Test value after upper boundary
1 ipset -T test 2.1.0.1
# Range: Try to add value before lower boundary
1 ipset -A test 2.0.0.0
# Range: Try to add value after upper boundary
1 ipset -A test 2.1.0.1
# Range: Delete element not added to the set
1 ipset -D test 2.0.0.2
# Range: Try to add value with MAC
0 ipset -A test 2.0.0.2,00:11:22:33:44:55
# Range: Test value with invalid MAC
1 ipset -T test 2.0.0.2,00:11:22:33:44:56
# Range: Test value with valid MAC
0 ipset -T test 2.0.0.2,00:11:22:33:44:55
# Range: Add MAC to already added element
0 ipset -A test 2.0.0.1,00:11:22:33:44:56
# Range: Test value without supplying MAC
0 ipset -T test 2.0.0.1
# Range: Test value with valid MAC
0 ipset -T test 2.0.0.1,00:11:22:33:44:56
# Range: Add an element in the middle
0 ipset -A test 2.0.200.214,00:11:22:33:44:57
# Range: Delete the same element
0 ipset -D test 2.0.200.214
# Range: List set
0 ipset -L test > .foo
# Range: Check listing
0 diff -u -I 'Size in memory.*' .foo macipmap.t.list0
# Range: Flush test set
0 ipset -F test
# Range: Delete test set
0 ipset -X test
# Network: Try to create a set from an invalid network
1 ipset -N test macipmap --network 2.0.0.0/15
# Network: Create a set from a valid network
0 ipset -N test macipmap --network 2.0.0.1/16
# Network: Add lower boundary
0 ipset -A test 2.0.0.0
# Network: Add upper boundary
0 ipset -A test 2.0.255.255
# Network: Test lower boundary
0 ipset -T test 2.0.0.0
# Network: Test upper boundary
0 ipset -T test 2.0.255.255
# Network: Test value not added to the set
1 ipset -T test 2.0.0.1
# Network: Test value before lower boundary
1 ipset -T test 1.255.255.255
# Network: Test value after upper boundary
1 ipset -T test 2.1.0.0
# Network: Try to add value before lower boundary
1 ipset -A test 1.255.255.255
# Network: Try to add value after upper boundary
1 ipset -A test 2.1.0.0
# Network: Delete element not added to the set
1 ipset -D test 2.0.0.2
# Network: Try to add value with MAC
0 ipset -A test 2.0.0.2,00:11:22:33:44:55
# Network: Test value with invalid MAC
1 ipset -T test 2.0.0.2,00:11:22:33:44:56
# Network: Test value with valid MAC
0 ipset -T test 2.0.0.2,00:11:22:33:44:55
# Network: Add MAC to already added element
0 ipset -A test 2.0.255.255,00:11:22:33:44:56
# Network: List set
0 ipset -L test > .foo
# Network: Check listing
0 diff -u -I 'Size in memory.*' .foo macipmap.t.list1
# Network: Flush test set
0 ipset -F test
# Network: Delete test set
0 ipset -X test
# Range: Create a set from a valid range with timeout
0 ipset -N test macipmap --from 2.0.0.1 --to 2.1.0.0 timeout 5
# Range: Add lower boundary
0 ipset -A test 2.0.0.1 timeout 4
# Range: Add upper boundary
0 ipset -A test 2.1.0.0 timeout 3
# Range: Test lower boundary
0 ipset -T test 2.0.0.1
# Range: Test upper boundary
0 ipset -T test 2.1.0.0
# Range: Test value not added to the set
1 ipset -T test 2.0.0.2
# Range: Test value before lower boundary
1 ipset -T test 2.0.0.0
# Range: Test value after upper boundary
1 ipset -T test 2.1.0.1
# Range: Try to add value before lower boundary
1 ipset -A test 2.0.0.0
# Range: Try to add value after upper boundary
1 ipset -A test 2.1.0.1
# Range: Try to add value with MAC
0 ipset -A test 2.0.0.2,00:11:22:33:44:55 timeout 4
# Range: Test value with invalid MAC
1 ipset -T test 2.0.0.2,00:11:22:33:44:56
# Range: Test value with valid MAC
0 ipset -T test 2.0.0.2,00:11:22:33:44:55
# Range: Add MAC to already added element
0 ipset -A test 2.0.0.1,00:11:22:33:44:56
# Range: Add an element in the middle
0 ipset -A test 2.0.200.214,00:11:22:33:44:57
# Range: Delete the same element
0 ipset -D test 2.0.200.214
# Range: List set
0 ipset -L test | sed 's/timeout ./timeout x/' > .foo
# Range: Check listing
0 diff -u -I 'Size in memory.*' .foo macipmap.t.list3
# Range: sleep 5s so that elements can timeout
0 sleep 5
# Range: List set
0 ipset -L test | sed 's/timeout ./timeout x/' > .foo
# Range: Check listing
0 diff -u -I 'Size in memory.*' .foo macipmap.t.list2
# Range: Flush test set
0 ipset -F test
# Range: add element with 1s timeout
0 ipset add test 2.0.200.214,00:11:22:33:44:57 timeout 1
# Range: readd element with 3s timeout
0 ipset add test 2.0.200.214,00:11:22:33:44:57 timeout 3 -exist
# Range: sleep 2s
0 sleep 2s
# Range: check readded element
0 ipset test test 2.0.200.214
# Range: Delete test set
0 ipset -X test
# eof
