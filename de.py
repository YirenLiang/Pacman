whole_map[int(i[0]), int(i[1])] = -50
                    ghosts_reach1 = []
                    ghosts_reach2 = []
                    ghosts_reach3 = []
                    ghosts_reach4 = []
                    reached = []
                    if whole_map[int(i[0]) - 1, int(i[1])] != "#":
                        ghosts_reach1.append((int(i[0]) - 1, int(i[1])))
                    if whole_map[int(i[0]) + 1, int(i[1])] != "#":
                        ghosts_reach1.append((int(i[0]) + 1, int(i[1])))
                    if whole_map[int(i[0]), int(i[1]) + 1] != "#":
                        ghosts_reach1.append((int(i[0]), int(i[1]) + 1))
                    if whole_map[int(i[0]), int(i[1]) - 1] != "#":
                        ghosts_reach1.append((int(i[0]), int(i[1]) - 1))
                    reached = reached + ghosts_reach1
                    for j in ghosts_reach1:
                        if whole_map[j[0] - 1, j[1]] != "#" and (j[0] - 1, j[1]) not in reached:
                            ghosts_reach2.append((j[0] - 1, j[1]))
                            reached.append((j[0] - 1, j[1]))
                        if whole_map[j[0] + 1, j[1]] != "#" and (j[0] + 1, j[1]) not in reached:
                            ghosts_reach2.append((j[0] + 1, j[1]))
                            reached.append((j[0] + 1, j[1]))
                        if whole_map[j[0], j[1] - 1] != "#" and (j[0], j[1] - 1) not in reached:
                            ghosts_reach2.append((j[0], j[1] - 1))
                            reached.append((j[0], j[1] - 1))
                        if whole_map[j[0], j[1] + 1] != "#" and (j[0], j[1] + 1) not in reached:
                            ghosts_reach2.append((j[0], j[1] + 1))
                            reached.append((j[0], j[1] + 1))
                    for k in ghosts_reach2:
                        if whole_map[k[0] - 1, k[1]] != "#" and (k[0] - 1, k[1]) not in reached:
                            ghosts_reach3.append((k[0] - 1, k[1]))
                            reached.append((k[0] - 1, k[1]))
                        if whole_map[k[0] + 1, k[1]] != "#" and (k[0] + 1, k[1]) not in reached:
                            ghosts_reach3.append((k[0] + 1, k[1]))
                            reached.append((k[0] + 1, k[1]))
                        if whole_map[k[0], k[1] - 1] != "#" and (k[0], k[1] - 1) not in reached:
                            ghosts_reach3.append((k[0], k[1] - 1))
                            reached.append((k[0], k[1] - 1))
                        if whole_map[k[0], k[1] + 1] != "#" and (k[0], k[1] + 1) not in reached:
                            ghosts_reach3.append((k[0], k[1] + 1))
                            reached.append((k[0], k[1] + 1))
                    for f in ghosts_reach3:
                        if whole_map[f[0] - 1, f[1]] != "#" and (f[0] - 1, f[1]) not in reached:
                            ghosts_reach4.append((f[0] - 1, f[1]))
                            reached.append((f[0] - 1, f[1]))
                        if whole_map[f[0] + 1, f[1]] != "#" and (f[0] + 1, f[1]) not in reached:
                            ghosts_reach4.append((f[0] + 1, f[1]))
                            reached.append((f[0] + 1, f[1]))
                        if whole_map[f[0], f[1] - 1] != "#" and (f[0], f[1] - 1) not in reached:
                            ghosts_reach4.append((f[0], f[1] - 1))
                            reached.append((f[0], f[1] - 1))
                        if whole_map[f[0], f[1] + 1] != "#" and (f[0], f[1] + 1) not in reached:
                            ghosts_reach4.append((f[0], f[1] + 1))
                            reached.append((f[0], f[1] + 1))
                    for x in ghosts_reach1:
                        whole_map[x[0], x[1]] = -40
                    for y in ghosts_reach2:
                        whole_map[y[0], y[1]] = -30
                    for z in ghosts_reach3:
                        whole_map[z[0], z[1]] = -20
                    for w in ghosts_reach4:
                        whole_map[w[0], w[1]] = -10