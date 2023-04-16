package gradu.gradu.domain;

import lombok.*;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
@Builder
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
public class Member {

    @Id @GeneratedValue
    @Column(name="member_id")
    private Long id;

    private String userID;

    private String userPassID;

    private String userName;

    private String userGender;

    private String userEmail;

    private String userCode;

    @OneToMany(mappedBy = "member")
    private List<Board>  boards = new ArrayList<>();
}
